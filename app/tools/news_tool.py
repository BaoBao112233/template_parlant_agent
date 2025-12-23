"""News headlines tool."""
import aiohttp
import parlant.sdk as p
from datetime import datetime


@p.tool
async def get_news_headlines(context: p.ToolContext, category: str = "general") -> p.ToolResult:
    """
    Get latest news headlines by category.
    
    Args:
        category: News category (general, technology, business, health, science, sports, entertainment)
        
    Returns:
        Latest news headlines
    """
    try:
        # Using NewsAPI.org free tier (requires API key for full functionality)
        # For demo purposes, providing sample news
        categories_map = {
            "general": "📰 General News",
            "technology": "💻 Technology News",
            "business": "💼 Business News",
            "health": "🏥 Health News",
            "science": "🔬 Science News",
            "sports": "⚽ Sports News",
            "entertainment": "🎬 Entertainment News"
        }
        
        category_lower = category.lower()
        if category_lower not in categories_map:
            category_lower = "general"
        
        # Sample news structure (in production, use actual API)
        result = f"{categories_map[category_lower]} - Latest Headlines:\n\n"
        result += "💡 To get real-time news, please configure NEWS_API_KEY in your .env file\n"
        result += "Get your free API key at: https://newsapi.org/\n\n"
        result += "Sample headlines:\n"
        result += f"1. Breaking: Major developments in {category_lower}\n"
        result += f"2. Expert analysis on current {category_lower} trends\n"
        result += f"3. In-depth: What's happening in {category_lower} today\n"
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error fetching news: {str(e)}")
