# 🤖 Parlant Lifestyle Agent - Tools Reference

Quick reference for all available tools in the agent.

## 🌤️ Weather Tools

### get_weather
Get current weather information for any city.

**Parameters:**
- `city` (str): Name of the city

**Example:**
```
"What's the weather in Tokyo?"
"How's the weather in London today?"
```

---

## 🍳 Recipe Tools

### search_recipes
Search for recipes by ingredient.

**Parameters:**
- `ingredient` (str): Main ingredient to search for
- `cuisine` (str, optional): Type of cuisine

**Example:**
```
"Find me recipes with chicken"
"Show me Italian recipes with tomatoes"
```

### get_recipe_details
Get detailed instructions for a specific recipe.

**Parameters:**
- `recipe_id` (str): The recipe ID

**Example:**
```
"Show me details for recipe 52772"
```

---

## 💪 Fitness Tools

### calculate_bmi
Calculate Body Mass Index.

**Parameters:**
- `weight_kg` (float): Weight in kilograms
- `height_cm` (float): Height in centimeters

**Example:**
```
"Calculate my BMI: 70kg, 175cm"
"What's the BMI for 65kg and 160cm?"
```

### calculate_calories
Estimate calories burned during activity.

**Parameters:**
- `activity` (str): Type of activity
- `duration_minutes` (int): Duration in minutes
- `weight_kg` (float): Body weight

**Example:**
```
"How many calories burned running for 30 minutes at 70kg?"
"Calculate calories for 45 minutes of cycling at 65kg"
```

### water_intake_reminder
Calculate recommended daily water intake.

**Parameters:**
- `weight_kg` (float): Body weight

**Example:**
```
"How much water should I drink? I weigh 70kg"
"Daily water intake for 65kg?"
```

---

## 💱 Currency Tool

### convert_currency
Convert between different currencies.

**Parameters:**
- `amount` (float): Amount to convert
- `from_currency` (str): Source currency code
- `to_currency` (str): Target currency code

**Example:**
```
"Convert 100 USD to EUR"
"How much is 1000 VND in USD?"
```

---

## 🕐 Date/Time Tools

### get_datetime
Get current date and time for a timezone.

**Parameters:**
- `timezone` (str): Timezone name (default: UTC)

**Example:**
```
"What time is it in Tokyo?"
"Current time in New York"
```

### calculate_age
Calculate age from birth date.

**Parameters:**
- `birth_date` (str): Birth date (YYYY-MM-DD)

**Example:**
```
"How old am I? Born 1990-05-15"
"Calculate age for 2000-12-25"
```

### days_between_dates
Calculate days between two dates.

**Parameters:**
- `start_date` (str): Start date (YYYY-MM-DD)
- `end_date` (str): End date (YYYY-MM-DD)

**Example:**
```
"Days between 2024-01-01 and 2024-12-31"
"How many days from 2024-06-01 to 2024-12-25?"
```

---

## 🌍 Translation Tool

### translate_text
Translate text to another language.

**Parameters:**
- `text` (str): Text to translate
- `target_language` (str): Target language code

**Example:**
```
"Translate 'Hello' to Vietnamese"
"How do you say 'Thank you' in French?"
```

**Supported Languages:**
- vi: Vietnamese
- en: English
- es: Spanish
- fr: French
- de: German
- ja: Japanese
- zh: Chinese
- ko: Korean

---

## 🎲 Random Tools

### flip_coin
Flip a coin for random decision.

**Example:**
```
"Flip a coin"
"Heads or tails?"
```

### roll_dice
Roll dice with specified sides.

**Parameters:**
- `sides` (int): Number of sides (default: 6)
- `count` (int): Number of dice (default: 1)

**Example:**
```
"Roll a dice"
"Roll 2 six-sided dice"
"Roll 3d20"
```

### random_number
Generate random number in range.

**Parameters:**
- `min_value` (int): Minimum value
- `max_value` (int): Maximum value

**Example:**
```
"Random number between 1 and 100"
"Pick a random number from 1 to 50"
```

### pick_random_choice
Pick random option from list.

**Parameters:**
- `options` (str): Comma-separated options

**Example:**
```
"Choose between pizza, burger, sushi"
"Pick one: red, blue, green"
```

---

## 📰 News Tool

### get_news_headlines
Get latest news by category.

**Parameters:**
- `category` (str): News category

**Example:**
```
"Show me technology news"
"Latest sports headlines"
```

**Categories:**
- general
- technology
- business
- health
- science
- sports
- entertainment

---

## ✨ Inspiration Tool

### get_daily_quote
Get an inspirational quote.

**Example:**
```
"Give me a motivational quote"
"I need some inspiration"
"Daily quote please"
```

---

## 🎯 Tips for Best Results

1. **Be Specific**: Provide all required parameters
2. **Natural Language**: Use conversational queries
3. **Units**: Specify units (kg, cm, minutes, etc.)
4. **Formats**: Use correct date format (YYYY-MM-DD)
5. **Currency Codes**: Use standard 3-letter codes (USD, EUR, VND)

## 🔄 Combining Tools

The agent can intelligently use multiple tools:

```
"What's the weather in Paris and convert 100 EUR to USD"
"Calculate my BMI (70kg, 175cm) and recommended water intake"
"Translate 'Good morning' to Vietnamese and Japanese"
```

---

For more information, see the [API Documentation](API.md).
