"""Translation tool."""
import aiohttp
import parlant.sdk as p


@p.tool
async def translate_text(context: p.ToolContext, text: str, target_language: str) -> p.ToolResult:
    """
    Translate text to a target language.
    
    Args:
        text: Text to translate
        target_language: Target language code (e.g., vi, en, es, fr, de, ja, zh)
        
    Returns:
        Translated text
    """
    try:
        # Using MyMemory Translation API (free tier)
        async with aiohttp.ClientSession() as session:
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": f"en|{target_language}"
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    translated = data.get('responseData', {}).get('translatedText', '')
                    
                    result = (
                        f"🌍 Translation:\n"
                        f"Original: {text}\n"
                        f"Language: {target_language.upper()}\n"
                        f"Translated: {translated}"
                    )
                    
                    return p.ToolResult(result)
                else:
                    return p.ToolResult(f"❌ Could not translate text")
    except Exception as e:
        return p.ToolResult(f"❌ Error translating text: {str(e)}")
