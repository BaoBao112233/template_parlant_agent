"""Parlant agent setup with Vertex AI Gemini integration."""
import asyncio
from typing import Optional
import parlant.sdk as p
from vertexai.generative_models import GenerativeModel

from app.config.settings import settings
from app.config.vertex_ai import initialize_vertex_ai, get_vertex_ai_model_name
from app.tools import (
    get_weather,
    search_recipes,
    get_recipe_details,
    calculate_bmi,
    calculate_calories,
    water_intake_reminder,
    convert_currency,
    get_datetime,
    calculate_age,
    days_between_dates,
    translate_text,
    flip_coin,
    roll_dice,
    random_number,
    pick_random_choice,
    get_news_headlines,
    get_daily_quote,
)


class ParlantAgent:
    """Parlant agent with Vertex AI Gemini integration."""
    
    def __init__(self):
        self.server: Optional[p.Server] = None
        self.agent: Optional[p.Agent] = None
        
    async def initialize(self):
        """Initialize Vertex AI and create the Parlant agent."""
        
        # Initialize Vertex AI
        initialize_vertex_ai()
        
        # Create Parlant server with Vertex AI Gemini NLP service
        # Use vertex or gemini NLP service (both work with Vertex AI)
        self.server = p.Server(
            nlp_service=p.NLPServices.vertex,  # or p.NLPServices.gemini
            port=8800,
        )
        
        await self.server.__aenter__()
        
        # Create agent with Gemini model
        self.agent = await self.server.create_agent(
            name=settings.AGENT_NAME,
            description=settings.AGENT_DESCRIPTION,
        )
        
        # Configure agent to use Vertex AI Gemini
        await self._setup_guidelines()
        await self._setup_context_variables()
        
        print(f"✅ Agent '{settings.AGENT_NAME}' initialized successfully!")
        print(f"🌐 Web UI available at: http://localhost:8000")
        
        return self.agent
    
    async def _setup_guidelines(self):
        """Setup agent behavioral guidelines."""
        
        # Weather guideline
        await self.agent.create_guideline(
            condition="User asks about weather or temperature in a city",
            action="Use the get_weather tool to fetch current weather information and provide a friendly response",
            tools=[get_weather]
        )
        
        # Recipe guidelines
        await self.agent.create_guideline(
            condition="User wants recipe ideas or asks about cooking with specific ingredients",
            action="Search for recipes using the search_recipes tool and suggest options",
            tools=[search_recipes]
        )
        
        await self.agent.create_guideline(
            condition="User wants detailed recipe instructions",
            action="Get recipe details using the get_recipe_details tool with the recipe ID",
            tools=[get_recipe_details]
        )
        
        # Fitness guidelines
        await self.agent.create_guideline(
            condition="User wants to calculate BMI or check their body mass index",
            action="Use calculate_bmi tool with weight and height to provide BMI information",
            tools=[calculate_bmi]
        )
        
        await self.agent.create_guideline(
            condition="User asks about calories burned during exercise or activity",
            action="Use calculate_calories tool to estimate calories burned based on activity, duration, and weight",
            tools=[calculate_calories]
        )
        
        await self.agent.create_guideline(
            condition="User asks about daily water intake or hydration recommendations",
            action="Use water_intake_reminder tool to calculate recommended daily water intake",
            tools=[water_intake_reminder]
        )
        
        # Currency guideline
        await self.agent.create_guideline(
            condition="User wants to convert currency or asks about exchange rates",
            action="Use convert_currency tool to convert between different currencies",
            tools=[convert_currency]
        )
        
        # Date/Time guidelines
        await self.agent.create_guideline(
            condition="User asks about current time or date in a timezone",
            action="Use get_datetime tool to provide current date and time",
            tools=[get_datetime]
        )
        
        await self.agent.create_guideline(
            condition="User wants to calculate their age or someone's age",
            action="Use calculate_age tool with the birth date",
            tools=[calculate_age]
        )
        
        await self.agent.create_guideline(
            condition="User asks about the difference between two dates",
            action="Use days_between_dates tool to calculate the number of days",
            tools=[days_between_dates]
        )
        
        # Translation guideline
        await self.agent.create_guideline(
            condition="User wants to translate text to another language",
            action="Use translate_text tool to translate the text",
            tools=[translate_text]
        )
        
        # Random/Entertainment guidelines
        await self.agent.create_guideline(
            condition="User wants to flip a coin or make a binary decision",
            action="Use flip_coin tool to randomly select heads or tails",
            tools=[flip_coin]
        )
        
        await self.agent.create_guideline(
            condition="User wants to roll dice",
            action="Use roll_dice tool with the specified number of sides and count",
            tools=[roll_dice]
        )
        
        await self.agent.create_guideline(
            condition="User wants a random number in a range",
            action="Use random_number tool with min and max values",
            tools=[random_number]
        )
        
        await self.agent.create_guideline(
            condition="User wants help choosing between options or making a decision",
            action="Use pick_random_choice tool with comma-separated options",
            tools=[pick_random_choice]
        )
        
        # News guideline
        await self.agent.create_guideline(
            condition="User asks about news or current headlines",
            action="Use get_news_headlines tool to fetch latest news in the requested category",
            tools=[get_news_headlines]
        )
        
        # Quote guideline
        await self.agent.create_guideline(
            condition="User wants inspiration, motivation, or a quote",
            action="Use get_daily_quote tool to provide an inspirational quote",
            tools=[get_daily_quote]
        )
        
        # General behavior guideline
        await self.agent.create_guideline(
            condition="User greets or says hello",
            action="Greet warmly and introduce yourself as a lifestyle assistant. Mention some of your capabilities like weather, recipes, fitness, currency conversion, and more",
            tools=[]
        )
        
    async def _setup_context_variables(self):
        """Setup context variables for the agent."""
        
        # Current datetime context
        await self.agent.create_variable(
            name="current-datetime",
            tool=get_datetime
        )
    
    async def chat(self, customer_id: str, message: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            customer_id: Unique identifier for the customer/session  
            message: The user's message
            
        Returns:
            The agent's response text
        """
        if not self.agent:
            raise RuntimeError("Agent not initialized")
        
        try:
            # For now, simulate agent response by describing what tools it has
            # In production, you would integrate with Parlant's conversation API
            
            # Simple keyword matching to demonstrate tool usage
            message_lower = message.lower()
            
            if 'weather' in message_lower:
                return "🌤️ I can help you check the weather! Please tell me which city you'd like to know about. For example: 'What's the weather in Hanoi?'"
            
            elif 'recipe' in message_lower or 'cook' in message_lower:
                return "🍳 I can help you find recipes! Tell me what ingredient you'd like to cook with, and I'll search for delicious recipes."
            
            elif 'bmi' in message_lower or 'fitness' in message_lower:
                return "💪 I can calculate your BMI and provide fitness insights! Please provide your weight (kg) and height (cm). For example: 'Calculate BMI for 70kg and 175cm'"
            
            elif 'currency' in message_lower or 'convert' in message_lower:
                return "💱 I can convert currencies for you! Tell me the amount and currencies. For example: 'Convert 100 USD to VND'"
            
            elif 'translate' in message_lower:
                return "🌍 I can translate text for you! Tell me what to translate and to which language. For example: 'Translate Hello to Vietnamese'"
            
            elif 'coin' in message_lower or 'dice' in message_lower or 'random' in message_lower:
                return "🎲 I can help you make random decisions! Try: 'Flip a coin', 'Roll a dice', or 'Pick between pizza, sushi, burger'"
            
            elif 'news' in message_lower:
                return "📰 I can fetch the latest news for you! What category interests you? (technology, business, sports, entertainment, etc.)"
            
            elif 'quote' in message_lower or 'motivation' in message_lower:
                return "✨ Here's an inspirational quote for you: 'The only way to do great work is to love what you do.' - Steve Jobs"
            
            elif 'hello' in message_lower or 'hi' in message_lower:
                return f"👋 Hello! I'm {settings.AGENT_NAME}, your AI lifestyle assistant powered by Google Gemini 2.0 Flash.\n\nI have 10+ tools to help you with:\n🌤️ Weather forecasts\n🍳 Recipe search\n💪 Fitness calculations\n💱 Currency conversion\n🕐 Date & time tools\n🌍 Translation\n🎲 Random decisions\n📰 News headlines\n✨ Inspirational quotes\n\nHow can I help you today?"
            
            elif 'what can you do' in message_lower or 'help' in message_lower or 'capabilities' in message_lower:
                return "🤖 I'm your AI lifestyle assistant with these capabilities:\n\n🌤️ **Weather** - Get current weather for any city\n🍳 **Recipes** - Search recipes by ingredient\n💪 **Fitness** - Calculate BMI, calories, water intake\n💱 **Currency** - Convert between currencies\n🕐 **Date & Time** - Timezone info, age calculator\n🌍 **Translation** - Translate text to any language\n🎲 **Random** - Flip coins, roll dice, make choices\n📰 **News** - Latest headlines by category\n✨ **Quotes** - Daily inspiration\n\nJust ask me anything!"
            
            else:
                return f"I received your message: '{message}'\n\n💡 I'm here to help with weather, recipes, fitness, currency conversion, translations, news, and more!\n\nTry asking me about:\n• Weather in a city\n• Recipes with an ingredient\n• Currency conversion\n• Or say 'help' to see all my capabilities!"
                
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
