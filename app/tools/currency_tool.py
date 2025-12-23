"""Currency conversion tool."""
import aiohttp
import parlant.sdk as p


@p.tool
async def convert_currency(context: p.ToolContext, amount: float, from_currency: str, to_currency: str) -> p.ToolResult:
    """
    Convert currency from one type to another.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code (e.g., USD, EUR, VND)
        to_currency: Target currency code (e.g., USD, EUR, VND)
        
    Returns:
        Converted amount
    """
    try:
        # Using exchangerate-api.com free tier
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        async with aiohttp.ClientSession() as session:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = data.get('rates', {})
                    
                    if to_currency not in rates:
                        return p.ToolResult(f"❌ Currency {to_currency} not found")
                    
                    rate = rates[to_currency]
                    converted_amount = amount * rate
                    
                    result = (
                        f"💱 Currency Conversion:\n"
                        f"{amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}\n"
                        f"Exchange rate: 1 {from_currency} = {rate:.4f} {to_currency}"
                    )
                    
                    return p.ToolResult(result)
                else:
                    return p.ToolResult(f"❌ Could not fetch exchange rates")
    except Exception as e:
        return p.ToolResult(f"❌ Error converting currency: {str(e)}")
