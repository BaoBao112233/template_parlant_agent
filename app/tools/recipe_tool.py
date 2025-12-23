"""Recipe search tool."""
import aiohttp
import parlant.sdk as p


@p.tool
async def search_recipes(context: p.ToolContext, ingredient: str, cuisine: str = "") -> p.ToolResult:
    """
    Search for recipes by ingredient and optional cuisine type.
    
    Args:
        ingredient: Main ingredient to search for
        cuisine: Optional cuisine type (e.g., Italian, Mexican, Asian)
        
    Returns:
        List of recipe suggestions
    """
    try:
        # Using TheMealDB free API
        async with aiohttp.ClientSession() as session:
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    meals = data.get('meals', [])
                    
                    if not meals:
                        return p.ToolResult(f"No recipes found with {ingredient}")
                    
                    # Limit to first 5 recipes
                    recipes = meals[:5]
                    result = f"🍳 Recipe suggestions with {ingredient}:\n\n"
                    
                    for idx, meal in enumerate(recipes, 1):
                        result += f"{idx}. {meal['strMeal']}\n"
                        result += f"   ID: {meal['idMeal']}\n\n"
                    
                    result += "💡 Ask me for details about any recipe by name!"
                    return p.ToolResult(result)
                else:
                    return p.ToolResult(f"❌ Could not search recipes")
    except Exception as e:
        return p.ToolResult(f"❌ Error searching recipes: {str(e)}")


@p.tool
async def get_recipe_details(context: p.ToolContext, recipe_id: str) -> p.ToolResult:
    """
    Get detailed recipe instructions by recipe ID.
    
    Args:
        recipe_id: The recipe ID to get details for
        
    Returns:
        Detailed recipe instructions and ingredients
    """
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    meals = data.get('meals', [])
                    
                    if not meals:
                        return p.ToolResult(f"Recipe not found")
                    
                    meal = meals[0]
                    result = f"📝 {meal['strMeal']}\n"
                    result += f"Category: {meal['strCategory']}\n"
                    result += f"Cuisine: {meal['strArea']}\n\n"
                    result += "Ingredients:\n"
                    
                    # Get ingredients
                    for i in range(1, 21):
                        ingredient = meal.get(f'strIngredient{i}')
                        measure = meal.get(f'strMeasure{i}')
                        if ingredient and ingredient.strip():
                            result += f"• {measure} {ingredient}\n"
                    
                    result += f"\nInstructions:\n{meal['strInstructions'][:500]}..."
                    
                    return p.ToolResult(result)
                else:
                    return p.ToolResult(f"❌ Could not get recipe details")
    except Exception as e:
        return p.ToolResult(f"❌ Error getting recipe details: {str(e)}")
