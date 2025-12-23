"""Quote inspiration tool."""
import random
import parlant.sdk as p


# Collection of inspirational quotes
QUOTES = [
    {
        "quote": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs"
    },
    {
        "quote": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon"
    },
    {
        "quote": "The future belongs to those who believe in the beauty of their dreams.",
        "author": "Eleanor Roosevelt"
    },
    {
        "quote": "It is during our darkest moments that we must focus to see the light.",
        "author": "Aristotle"
    },
    {
        "quote": "The only impossible journey is the one you never begin.",
        "author": "Tony Robbins"
    },
    {
        "quote": "In the end, we only regret the chances we didn't take.",
        "author": "Lewis Carroll"
    },
    {
        "quote": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "author": "Chinese Proverb"
    },
    {
        "quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill"
    },
    {
        "quote": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt"
    },
    {
        "quote": "The only limit to our realization of tomorrow will be our doubts of today.",
        "author": "Franklin D. Roosevelt"
    }
]


@p.tool
async def get_daily_quote(context: p.ToolContext) -> p.ToolResult:
    """
    Get a random inspirational quote.
    
    Returns:
        An inspirational quote with author
    """
    try:
        quote_data = random.choice(QUOTES)
        
        result = (
            f"✨ Daily Inspiration:\n\n"
            f'"{quote_data["quote"]}"\n\n'
            f"— {quote_data['author']}"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error getting quote: {str(e)}")
