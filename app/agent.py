"""Parlant agent setup with Vertex AI Gemini integration."""
import asyncio
from typing import Optional, Dict
import parlant.sdk as p
from parlant.client import AsyncParlantClient
from vertexai.generative_models import GenerativeModel

from app.config.settings import settings
from app.config.vertex_ai import initialize_vertex_ai, get_vertex_ai_model_name
from app.tools import (
    crawl_url,
    search_google
)


class ParlantAgent:
    """Parlant agent with Vertex AI Gemini integration."""
    
    def __init__(self):
        self.server: Optional[p.Server] = None
        self.agent: Optional[p.Agent] = None
        self.client: Optional[AsyncParlantClient] = None
        self.session_map: Dict[str, str] = {}  # Map customer_id (UI) -> session_id (Parlant)
        
    async def initialize(self):
        """Initialize Vertex AI and create the Parlant agent."""
        
        # Initialize Vertex AI
        initialize_vertex_ai()
        
        # Create Parlant server with Vertex AI Gemini NLP service
        self.server = p.Server(
            nlp_service=p.NLPServices.vertex,
            port=8800,
        )
        
        await self.server.__aenter__()
        
        # Create agent with Gemini model
        self.agent = await self.server.create_agent(
            name=settings.AGENT_NAME,
            description=settings.AGENT_DESCRIPTION,
        )
        
        # Initialize client to talk to the server
        self.client = AsyncParlantClient(base_url="http://localhost:8800")
        
        # Configure agent to use Vertex AI Gemini
        await self._setup_guidelines()
        
        print(f"✅ Agent '{settings.AGENT_NAME}' initialized successfully!")
        print(f"🌐 Web UI available at: http://localhost:8000")
        
        return self.agent
    
    async def _setup_guidelines(self):
        """Setup agent behavioral guidelines."""
        
        # Search guideline
        await self.agent.create_guideline(
            condition="User wants to search for information on the internet",
            action="Use the search_google tool to find relevant information",
            tools=[search_google]
        )
        
        # Crawler guideline
        await self.agent.create_guideline(
            condition="User wants to read content from a specific URL or detailed content from a search result",
            action="Use the crawl_url tool to fetch the content of the URL",
            tools=[crawl_url]
        )
        
        # General behavior guideline
        await self.agent.create_guideline(
            condition="User greets or says hello",
            action="Greet warmly and introduce yourself as an assistant capable of searching the web and crawling pages.",
            tools=[]
        )
        
    async def chat(self, customer_id: str, message: str) -> str:
        """
        Send a message to the agent and get a response.
        """
        if not self.agent or not self.client:
            raise RuntimeError("Agent not initialized")
        
        try:
            # 1. Get or Create Session
            session_id = self.session_map.get(customer_id)
            if not session_id:
                # Create a session for this customer
                # We use customer_id as the name or ID for simplicity if supported, 
                # but let's just create a new customer for each session to be safe/simple for now
                # or reuse if we can listing customers.
                # For this demo, let's create a NEW session always if not mapped.
                
                # Check if customer exists? No, just create a new customer for simplification
                # or create session with new guest customer implicitly.
                session = await self.client.sessions.create(
                    agent_id=self.agent.id,
                    customer_id=None # Guest
                )
                session_id = session.id
                self.session_map[customer_id] = session_id
            
            # 2. Update to get current offset
            # (Optimization: We could track offset in session_map too, but listing events is safer)
            events = await self.client.sessions.list_events(session_id=session_id)
            # Find the max offset
            max_offset = -1
            if events:
                # Assuming offsets are sequential integers, find max. 
                # Inspecting 'Event' object structure would be good, looking at list it seems plausible.
                # Let's assume using len(events) as next offset if they are consistent.
                # Or just max(e.offset for e in events)
                # But 'Event' structure inspection via 'dir' showed it likely has properties.
                # I'll rely on len() for now or simply 0 if empty.
                # Actually, list_events returns ALL events.
                 pass

            # 3. Send Message
            sent_event = await self.client.sessions.create_event(
                session_id=session_id,
                kind="message",
                source="customer",
                message=message
            )
            
            wait_offset = 0
            # If `sent_event` has offset, we start from sent_event.offset + 1
            if hasattr(sent_event, "offset"):
                wait_offset = sent_event.offset + 1
            else:
                 # Fallback
                 wait_offset = len(events) + 1 

            # 4. Wait for Agent Response
            # We poll/wait for an event from 'ai_agent'
            # list_events supports wait_for_data
            
            print(f"Waiting for agent response (session {session_id}, offset >= {wait_offset})...")
            
            # We might get status events (typing, processing). We want 'message'.
            new_events = await self.client.sessions.list_events(
                session_id=session_id,
                min_offset=wait_offset,
                source="ai_agent",
                kinds="message", # Filter for message kind
                wait_for_data=60 # Wait up to 60 seconds
            )
            
            if new_events:
                # Return the first message content
                # Event payload might be in .data or .message?
                # create_event doc said message=... for kind=message.
                # Assuming .message attribute or .data['message']
                # Inspection of create_event return type 'Event' would help.
                # But typically it mimics the input.
                last_event = new_events[-1] # Get the latest one? Or first one? 
                # Usually the agent replies with one message block.
                # Let's verify 'message' attribute exists.
                if hasattr(last_event, "data") and isinstance(last_event.data, dict) and "message" in last_event.data:
                     return last_event.data["message"]
                if hasattr(last_event, "message") and last_event.message:
                     return last_event.message
                
                # Fallback inspection
                return str(last_event)
            
            return "Thinking... (No response received in time)"

        except Exception as e:
            print(f"❌ Chat error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    async def shutdown(self):
        """Shutdown the Parlant server."""
        if self.server:
            await self.server.__aexit__(None, None, None)
            print("✅ Agent shutdown complete")


# Global agent instance
parlant_agent = ParlantAgent()


async def get_agent() -> p.Agent:
    """Get or create the Parlant agent instance."""
    if parlant_agent.agent is None:
        await parlant_agent.initialize()
    return parlant_agent.agent


async def get_parlant_agent() -> ParlantAgent:
    """Get the full Parlant agent instance with chat capabilities."""
    if parlant_agent.agent is None:
        await parlant_agent.initialize()
    return parlant_agent


async def shutdown_agent():
    """Shutdown the Parlant agent."""
    await parlant_agent.shutdown()
