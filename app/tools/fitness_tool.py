"""Fitness and health tools."""
import parlant.sdk as p
from datetime import datetime


@p.tool
async def calculate_bmi(context: p.ToolContext, weight_kg: float, height_cm: float) -> p.ToolResult:
    """
    Calculate Body Mass Index (BMI).
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        
    Returns:
        BMI value and category
    """
    try:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        # Determine category
        if bmi < 18.5:
            category = "Underweight"
            emoji = "⚠️"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            emoji = "✅"
        elif 25 <= bmi < 30:
            category = "Overweight"
            emoji = "⚠️"
        else:
            category = "Obese"
            emoji = "❌"
        
        result = (
            f"💪 BMI Calculation:\n"
            f"Weight: {weight_kg} kg\n"
            f"Height: {height_cm} cm\n"
            f"BMI: {bmi:.2f}\n"
            f"{emoji} Category: {category}"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error calculating BMI: {str(e)}")


@p.tool
async def calculate_calories(context: p.ToolContext, activity: str, duration_minutes: int, weight_kg: float) -> p.ToolResult:
    """
    Estimate calories burned for an activity.
    
    Args:
        activity: Type of activity (walking, running, cycling, swimming, etc.)
        duration_minutes: Duration in minutes
        weight_kg: Body weight in kilograms
        
    Returns:
        Estimated calories burned
    """
    try:
        # MET (Metabolic Equivalent of Task) values for common activities
        met_values = {
            "walking": 3.5,
            "jogging": 7.0,
            "running": 9.8,
            "cycling": 7.5,
            "swimming": 8.0,
            "yoga": 2.5,
            "weightlifting": 6.0,
            "dancing": 5.5,
            "hiking": 6.0,
            "basketball": 8.0
        }
        
        activity_lower = activity.lower()
        met = met_values.get(activity_lower, 5.0)  # Default MET if activity not found
        
        # Calories = MET * weight(kg) * duration(hours)
        calories = met * weight_kg * (duration_minutes / 60)
        
        result = (
            f"🔥 Calories Burned:\n"
            f"Activity: {activity.title()}\n"
            f"Duration: {duration_minutes} minutes\n"
            f"Weight: {weight_kg} kg\n"
            f"Estimated calories: {calories:.0f} kcal"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error calculating calories: {str(e)}")


@p.tool
async def water_intake_reminder(context: p.ToolContext, weight_kg: float) -> p.ToolResult:
    """
    Calculate recommended daily water intake.
    
    Args:
        weight_kg: Body weight in kilograms
        
    Returns:
        Recommended daily water intake
    """
    try:
        # General recommendation: 30-35 ml per kg of body weight
        water_ml = weight_kg * 35
        water_liters = water_ml / 1000
        glasses = water_ml / 250  # Assuming 250ml per glass
        
        result = (
            f"💧 Daily Water Intake Recommendation:\n"
            f"Body weight: {weight_kg} kg\n"
            f"Recommended: {water_liters:.2f} liters ({water_ml:.0f} ml)\n"
            f"That's approximately {glasses:.0f} glasses (250ml each)\n\n"
            f"💡 Tips:\n"
            f"• Drink more during exercise\n"
            f"• Increase intake in hot weather\n"
            f"• Drink before you feel thirsty"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error calculating water intake: {str(e)}")
