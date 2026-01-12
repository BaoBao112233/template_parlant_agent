"""Crawler tool for extracting content from URLs."""
import aiohttp
from bs4 import BeautifulSoup
import parlant.sdk as p
import json

@p.tool
async def crawl_url(context: p.ToolContext, url: str) -> p.ToolResult:
    """
    Crawls content from a specific URL.
    
    Args:
        url: The URL to crawl.
        
    Returns:
        JSON string containing the title and text content of the page.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                html = await response.text()
                
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "No Title"
        
        # Extract main text content (simple extraction)
        # Removing scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        result = {
            "url": url,
            "title": title.strip(),
            "content_length": len(text),
            "full_content": text[:20000] # Limit content to avoid token limits if necessary, though Parlant can handle large text, checking best practices. I'll just return full text but be mindful.
        }
        
        return p.ToolResult(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        return p.ToolResult(json.dumps({"error": str(e), "url": url}, ensure_ascii=False))
