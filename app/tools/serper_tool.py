"""Google Serper search tool."""
import aiohttp
import parlant.sdk as p
import json
from app.config.settings import settings

@p.tool
async def search_google(context: p.ToolContext, query: str) -> p.ToolResult:
    """
    Search Google using Serper API.
    
    Args:
        query: The search query.
        
    Returns:
        JSON string containing search results.
    """
    try:
        api_key = settings.SERPER_API_KEY
        if not api_key:
             return p.ToolResult(json.dumps({"error": "SERPER_API_KEY not configured"}, ensure_ascii=False))

        endpoint = "https://google.serper.dev/search"
        
        params = {
            "q": query,
            "hl": "vi",      # default to Vietnamese as per user locale preference often implied or set in test
            "gl": "vn"
        }

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
             async with session.post(endpoint, headers=headers, json=params) as response: # Serper usually uses POST for detailed JSON body but GET is also supported. The test file used GET with params. Let's check test/serper.py Usage again.
                # test/serper.py used GET with params. Let's stick to that IF possible, but Serper documentation usually recommends POST.
                # Re-checking test/serper.py: `requests.get(endpoint, params=params, headers=headers)`
                # OK, I will use GET to match the test file exactly.
                pass
             async with session.get(endpoint, headers=headers, params=params) as response:
                 if response.status != 200:
                     text = await response.text()
                     return p.ToolResult(json.dumps({"error": f"API Error: {response.status}", "details": text}, ensure_ascii=False))
                 
                 data = await response.json()
                 return p.ToolResult(json.dumps(data, ensure_ascii=False))

    except Exception as e:
        return p.ToolResult(json.dumps({"error": str(e)}, ensure_ascii=False))
