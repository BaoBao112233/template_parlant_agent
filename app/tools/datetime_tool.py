"""Date and time utilities tool."""
import parlant.sdk as p
from datetime import datetime, timedelta
import pytz


@p.tool
async def get_datetime(context: p.ToolContext, timezone: str = "UTC") -> p.ToolResult:
    """
    Get current date and time for a specific timezone.
    
    Args:
        timezone: Timezone name (e.g., UTC, Asia/Ho_Chi_Minh, America/New_York)
        
    Returns:
        Current date and time in the specified timezone
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        
        result = (
            f"🕐 Current Time:\n"
            f"Timezone: {timezone}\n"
            f"Date: {now.strftime('%Y-%m-%d')}\n"
            f"Time: {now.strftime('%H:%M:%S')}\n"
            f"Day: {now.strftime('%A')}"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error getting datetime: {str(e)}")


@p.tool
async def calculate_age(context: p.ToolContext, birth_date: str) -> p.ToolResult:
    """
    Calculate age from birth date.
    
    Args:
        birth_date: Birth date in format YYYY-MM-DD
        
    Returns:
        Age in years and days
    """
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.now()
        
        age_years = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        
        # Calculate next birthday
        next_birthday = datetime(today.year, birth.month, birth.day)
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, birth.month, birth.day)
        
        days_to_birthday = (next_birthday - today).days
        
        result = (
            f"🎂 Age Calculation:\n"
            f"Birth date: {birth_date}\n"
            f"Age: {age_years} years old\n"
            f"Next birthday in: {days_to_birthday} days"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error calculating age: {str(e)}")


@p.tool
async def days_between_dates(context: p.ToolContext, start_date: str, end_date: str) -> p.ToolResult:
    """
    Calculate days between two dates.
    
    Args:
        start_date: Start date in format YYYY-MM-DD
        end_date: End date in format YYYY-MM-DD
        
    Returns:
        Number of days between the dates
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        delta = end - start
        days = abs(delta.days)
        
        result = (
            f"📅 Date Difference:\n"
            f"From: {start_date}\n"
            f"To: {end_date}\n"
            f"Difference: {days} days\n"
            f"That's approximately {days // 7} weeks"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error calculating date difference: {str(e)}")
