# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production deployments, consider adding API key authentication or OAuth2.

## Endpoints

### Health Check

Check if the service is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Parlant Lifestyle Agent",
  "version": "1.0.0"
}
```

---

### Get Agent Information

Retrieve information about the agent and its capabilities.

**Endpoint:** `GET /api/agent/info`

**Response:**
```json
{
  "name": "LifestyleAssistant",
  "description": "A helpful lifestyle assistant with various daily life tools",
  "available_tools": [
    "Weather forecast",
    "Recipe search",
    "BMI calculator",
    "Calorie counter",
    "Currency converter",
    "Date/Time utilities",
    "Translation",
    "Random decisions (coin flip, dice)",
    "News headlines",
    "Daily inspiration quotes"
  ],
  "status": "active"
}
```

---

### Chat with Agent

Send a message to the agent and receive a response.

**Endpoint:** `POST /api/chat`

**Request Body:**
```json
{
  "message": "What's the weather in Tokyo?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "The agent's response text",
  "session_id": "session-id",
  "agent_name": "LifestyleAssistant"
}
```

**Example Requests:**

1. Weather Query:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What'\''s the weather in Tokyo?"
  }'
```

2. Recipe Search:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me recipes with chicken and rice"
  }'
```

3. BMI Calculation:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate my BMI. I weigh 70kg and I'\''m 175cm tall"
  }'
```

---

### List Available Tools

Get a list of all available tools with descriptions and examples.

**Endpoint:** `GET /api/tools`

**Response:**
```json
{
  "tools": {
    "weather": {
      "name": "Weather Forecast",
      "description": "Get current weather for any city",
      "example": "What's the weather in Hanoi?"
    },
    "recipes": {
      "name": "Recipe Search",
      "description": "Search recipes by ingredient and get cooking instructions",
      "example": "Find me recipes with chicken"
    },
    // ... more tools
  },
  "total_count": 9
}
```

---

## Tool Examples

### Weather Tool

**Query:** "What's the weather in Paris?"

**Response:**
```
🌤️ Weather in Paris:
Temperature: 15°C (59°F)
Feels like: 13°C
Conditions: Partly cloudy
Humidity: 65%
```

### Recipe Tool

**Query:** "Find recipes with tomatoes"

**Response:**
```
🍳 Recipe suggestions with tomatoes:

1. Tomato Pasta
   ID: 52772

2. Tomato Soup
   ID: 52773

...

💡 Ask me for details about any recipe by name!
```

### Fitness Tools

**BMI Query:** "Calculate BMI for 70kg and 175cm"

**Response:**
```
💪 BMI Calculation:
Weight: 70 kg
Height: 175 cm
BMI: 22.86
✅ Category: Normal weight
```

**Calorie Query:** "How many calories do I burn running for 30 minutes at 70kg?"

**Response:**
```
🔥 Calories Burned:
Activity: Running
Duration: 30 minutes
Weight: 70 kg
Estimated calories: 343 kcal
```

### Currency Tool

**Query:** "Convert 100 USD to EUR"

**Response:**
```
💱 Currency Conversion:
100.00 USD = 92.50 EUR
Exchange rate: 1 USD = 0.9250 EUR
```

### Translation Tool

**Query:** "Translate 'Hello, how are you?' to Vietnamese"

**Response:**
```
🌍 Translation:
Original: Hello, how are you?
Language: VI
Translated: Xin chào, bạn khỏe không?
```

### Random Tools

**Coin Flip:** "Flip a coin"
```
Coin flip result: Heads 🪙
```

**Dice Roll:** "Roll 2 six-sided dice"
```
🎲 Rolling 2d6:
Results: 4, 6
Total: 10
```

**Random Choice:** "Choose between pizza, burger, sushi"
```
🎲 Random Choice:
Options: pizza, burger, sushi
Selected: ✨ sushi ✨
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request format"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing chat: [error message]"
}
```

## Rate Limiting

Currently, there are no rate limits. For production use, consider implementing rate limiting using middleware like `slowapi`.

## WebSocket Support (Future)

WebSocket support for real-time chat will be added in future versions:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.onmessage = (event) => {
  console.log('Received:', event.data);
};
```

## Interactive API Documentation

When the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Best Practices

1. **Session Management**: Use consistent `session_id` for conversation continuity
2. **Error Handling**: Always handle potential errors in responses
3. **Message Format**: Be clear and specific in queries for best results
4. **Tool Selection**: The agent automatically selects appropriate tools based on context

## Example Integration (Python)

```python
import requests

def chat_with_agent(message: str, session_id: str = None):
    url = "http://localhost:8000/api/chat"
    payload = {
        "message": message,
        "session_id": session_id
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Example usage
result = chat_with_agent("What's the weather in Tokyo?")
print(result["response"])
```

## Example Integration (JavaScript)

```javascript
async function chatWithAgent(message, sessionId = null) {
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      session_id: sessionId
    })
  });
  
  return await response.json();
}

// Example usage
chatWithAgent("What's the weather in Tokyo?")
  .then(result => console.log(result.response));
```
