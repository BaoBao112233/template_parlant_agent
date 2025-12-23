"""FastAPI application for the Parlant Lifestyle Agent."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from app.config.settings import settings
from app.agent import get_agent, get_parlant_agent, shutdown_agent


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="A Parlant-powered lifestyle assistant with 10+ helpful tools"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic models
class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    agent_name: str


class AgentInfo(BaseModel):
    """Agent information model."""
    name: str
    description: str
    available_tools: List[str]
    status: str


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    try:
        await get_agent()
        print("🚀 FastAPI server started successfully!")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    await shutdown_agent()
    print("👋 FastAPI server shutdown complete")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the home page."""
    return FileResponse("static/index.html")


@app.get("/chat.html", response_class=HTMLResponse)
async def chat_page():
    """Serve the chat interface."""
    return FileResponse("static/chat.html")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }


@app.get("/api/agent/info", response_model=AgentInfo)
async def get_agent_info():
    """Get agent information and available tools."""
    try:
        agent = await get_agent()
        
        tools_list = [
            "Weather forecast",
            "Recipe search",
            "BMI calculator",
            "Calorie counter",
            "Currency converter",
            "Date/Time utilities",
            "Translation",
            "Random decisions (coin flip, dice)",
            "News headlines",
            "Daily inspiration quotes"
        ]
        
        return AgentInfo(
            name=settings.AGENT_NAME,
            description=settings.AGENT_DESCRIPTION,
            available_tools=tools_list,
            status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent info: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat endpoint to interact with the agent.
    
    This endpoint forwards messages to the Parlant agent and returns responses.
    """
    try:
        parlant_agent = await get_parlant_agent()
        
        # Create or get session
        session_id = message.session_id or f"session-{hash(str(message.message))}"
        
        # Chat with the agent
        response_text = await parlant_agent.chat(
            customer_id=session_id,
            message=message.message
        )
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            agent_name=settings.AGENT_NAME
        )
    except Exception as e:
        print(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.get("/api/tools")
async def list_tools():
    """List all available tools with descriptions."""
    tools = {
        "weather": {
            "name": "Weather Forecast",
            "description": "Get current weather for any city",
            "example": "What's the weather in Hanoi?"
        },
        "recipes": {
            "name": "Recipe Search",
            "description": "Search recipes by ingredient and get cooking instructions",
            "example": "Find me recipes with chicken"
        },
        "fitness": {
            "name": "Fitness Tools",
            "description": "BMI calculator, calorie counter, water intake recommendations",
            "example": "Calculate my BMI for 70kg and 175cm"
        },
        "currency": {
            "name": "Currency Converter",
            "description": "Convert between different currencies",
            "example": "Convert 100 USD to VND"
        },
        "datetime": {
            "name": "Date & Time",
            "description": "Get current time, calculate age, date differences",
            "example": "What time is it in Tokyo?"
        },
        "translation": {
            "name": "Translation",
            "description": "Translate text to different languages",
            "example": "Translate 'Hello' to Vietnamese"
        },
        "random": {
            "name": "Random Decisions",
            "description": "Flip coins, roll dice, pick random choices",
            "example": "Flip a coin for me"
        },
        "news": {
            "name": "News Headlines",
            "description": "Get latest news by category",
            "example": "Show me technology news"
        },
        "quotes": {
            "name": "Daily Inspiration",
            "description": "Get motivational quotes",
            "example": "Give me an inspirational quote"
        }
    }
    
    return {"tools": tools, "total_count": len(tools)}


def start_server():
    """Start the FastAPI server."""
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
