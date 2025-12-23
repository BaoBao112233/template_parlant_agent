"""Random decision and entertainment tools."""
import random
import parlant.sdk as p


@p.tool
async def flip_coin(context: p.ToolContext) -> p.ToolResult:
    """
    Flip a coin to make a random decision.
    
    Returns:
        Heads or Tails
    """
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    return p.ToolResult(f"Coin flip result: {result}")


@p.tool
async def roll_dice(context: p.ToolContext, sides: int = 6, count: int = 1) -> p.ToolResult:
    """
    Roll dice with specified number of sides.
    
    Args:
        sides: Number of sides on the dice (default: 6)
        count: Number of dice to roll (default: 1)
        
    Returns:
        Dice roll results
    """
    try:
        if count < 1 or count > 10:
            return p.ToolResult("❌ Please roll between 1 and 10 dice")
        
        if sides < 2 or sides > 100:
            return p.ToolResult("❌ Dice must have between 2 and 100 sides")
        
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)
        
        result = f"🎲 Rolling {count}d{sides}:\n"
        result += f"Results: {', '.join(map(str, rolls))}\n"
        result += f"Total: {total}"
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error rolling dice: {str(e)}")


@p.tool
async def random_number(context: p.ToolContext, min_value: int = 1, max_value: int = 100) -> p.ToolResult:
    """
    Generate a random number within a range.
    
    Args:
        min_value: Minimum value (default: 1)
        max_value: Maximum value (default: 100)
        
    Returns:
        Random number
    """
    try:
        if min_value >= max_value:
            return p.ToolResult("❌ Minimum value must be less than maximum value")
        
        number = random.randint(min_value, max_value)
        result = f"🎯 Random number between {min_value} and {max_value}: {number}"
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error generating random number: {str(e)}")


@p.tool
async def pick_random_choice(context: p.ToolContext, options: str) -> p.ToolResult:
    """
    Pick a random choice from a list of options.
    
    Args:
        options: Comma-separated list of options
        
    Returns:
        Randomly selected option
    """
    try:
        choices = [opt.strip() for opt in options.split(',') if opt.strip()]
        
        if not choices:
            return p.ToolResult("❌ Please provide at least one option")
        
        selected = random.choice(choices)
        
        result = (
            f"🎲 Random Choice:\n"
            f"Options: {', '.join(choices)}\n"
            f"Selected: ✨ {selected} ✨"
        )
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error picking random choice: {str(e)}")
