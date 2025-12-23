"""Weather information tool."""
import aiohttp
from datetime import datetime
import parlant.sdk as p
from app.config.settings import settings


@p.tool
async def get_weather(context: p.ToolContext, city: str) -> p.ToolResult:
    """
    Get current weather information for a city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Weather information including temperature, conditions, and humidity
    """
    try:
        # Using wttr.in as a free weather service (no API key needed)
        async with aiohttp.ClientSession() as session:
            url = f"https://wttr.in/{city}?format=j1"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data['current_condition'][0]
                    
                    temp_c = current['temp_C']
                    temp_f = current['temp_F']
                    description = current['weatherDesc'][0]['value']
                    humidity = current['humidity']
                    feels_like = current['FeelsLikeC']
                    
                    result = (
                        f"🌤️ Weather in {city}:\n"
                        f"Temperature: {temp_c}°C ({temp_f}°F)\n"
                        f"Feels like: {feels_like}°C\n"
                        f"Conditions: {description}\n"
                        f"Humidity: {humidity}%"
                    )
                    return p.ToolResult(result)
                else:
                    return p.ToolResult(f"❌ Could not fetch weather for {city}")
    except Exception as e:
        return p.ToolResult(f"❌ Error fetching weather: {str(e)}")
