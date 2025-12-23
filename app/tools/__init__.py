"""Tools module - exports all available tools."""
from app.tools.weather_tool import get_weather
from app.tools.recipe_tool import search_recipes, get_recipe_details
from app.tools.fitness_tool import calculate_bmi, calculate_calories, water_intake_reminder
from app.tools.currency_tool import convert_currency
from app.tools.datetime_tool import get_datetime, calculate_age, days_between_dates
from app.tools.translation_tool import translate_text
from app.tools.random_tool import flip_coin, roll_dice, random_number, pick_random_choice
from app.tools.news_tool import get_news_headlines
from app.tools.quote_tool import get_daily_quote

# Export all tools
__all__ = [
    # Weather
    "get_weather",
    
    # Recipes
    "search_recipes",
    "get_recipe_details",
    
    # Fitness
    "calculate_bmi",
    "calculate_calories",
    "water_intake_reminder",
    
    # Currency
    "convert_currency",
    
    # Date/Time
    "get_datetime",
    "calculate_age",
    "days_between_dates",
    
    # Translation
    "translate_text",
    
    # Random/Entertainment
    "flip_coin",
    "roll_dice",
    "random_number",
    "pick_random_choice",
    
    # News
    "get_news_headlines",
    
    # Inspiration
    "get_daily_quote",
]
