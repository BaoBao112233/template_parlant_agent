# Parlant Lifestyle Agent

A powerful AI agent built with [Parlant](https://github.com/emcie-co/parlant) framework, featuring 10+ lifestyle tools powered by Google Vertex AI Gemini 2.0 Flash.

## 🌟 Features

- **10+ Lifestyle Tools**: Weather, recipes, fitness calculators, currency conversion, and more
- **Vertex AI Integration**: Powered by Google's Gemini 2.0 Flash model
- **FastAPI Backend**: RESTful API with async support
- **Web Interface**: Beautiful, responsive web UI
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Behavioral Guidelines**: Parlant ensures consistent, reliable agent behavior

## 🛠️ Available Tools

1. **Weather Forecast** - Get real-time weather for any city
2. **Recipe Search** - Find recipes by ingredient with detailed instructions
3. **BMI Calculator** - Calculate Body Mass Index
4. **Calorie Counter** - Estimate calories burned during activities
5. **Water Intake** - Daily hydration recommendations
6. **Currency Converter** - Convert between currencies with live rates
7. **Date/Time Utilities** - Timezone info, age calculator, date differences
8. **Translation** - Translate text between languages
9. **Random Tools** - Coin flip, dice roll, random choices
10. **News Headlines** - Latest news by category
11. **Daily Quotes** - Inspirational quotes

## 📋 Prerequisites

- Python 3.10+
- Docker and Docker Compose (for containerized deployment)
- Google Cloud service account with Vertex AI API enabled
- `service-account.json` file in project root

## 🚀 Quick Start

### Local Development

1. **Clone and setup**:
```bash
cd /path/to/template_parlant_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run the application**:
```bash
python -m app.main
```

4. **Access the interfaces**:
- Web UI: http://localhost:8000
- Parlant Playground: http://localhost:8800
- API Docs: http://localhost:8000/docs

### Docker Deployment

1. **Build and run**:
```bash
docker-compose up -d
```

2. **Check status**:
```bash
docker-compose ps
docker-compose logs -f
```

3. **Stop**:
```bash
docker-compose down
```

## 📁 Project Structure

```
template_parlant_agent/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py        # Application settings
│   │   └── vertex_ai.py       # Vertex AI configuration
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather_tool.py
│   │   ├── recipe_tool.py
│   │   ├── fitness_tool.py
│   │   ├── currency_tool.py
│   │   ├── datetime_tool.py
│   │   ├── translation_tool.py
│   │   ├── random_tool.py
│   │   ├── news_tool.py
│   │   └── quote_tool.py
│   ├── __init__.py
│   ├── agent.py               # Parlant agent setup
│   └── main.py                # FastAPI application
├── docs/
│   ├── README.md              # This file
│   ├── API.md                 # API documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── DEVELOPMENT.md         # Development guide
├── static/
│   └── index.html             # Web interface
├── .env.example               # Environment variables template
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── requirements.txt
└── service-account.json       # Your GCP service account key
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Parlant Settings
PARLANT_HOST=0.0.0.0
PARLANT_PORT=8800

# Vertex AI Settings
VERTEX_AI_PROJECT_ID=your-project-id
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-2.0-flash-exp

# Agent Settings
AGENT_NAME=LifestyleAssistant
AGENT_DESCRIPTION=A helpful lifestyle assistant with various daily life tools

# Optional API Keys
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key
```

### Service Account Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new service account or use existing one
3. Grant "Vertex AI User" role
4. Create and download JSON key
5. Save as `service-account.json` in project root

## 📖 API Documentation

### Health Check
```bash
GET /api/health
```

### Agent Information
```bash
GET /api/agent/info
```

### Chat with Agent
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "What's the weather in Tokyo?",
  "session_id": "optional-session-id"
}
```

### List Tools
```bash
GET /api/tools
```

For detailed API documentation, visit http://localhost:8000/docs when the server is running.

## 🐳 Docker Details

### Build Custom Image
```bash
docker build -t parlant-lifestyle-agent .
```

### Run Container
```bash
docker run -p 8000:8000 -p 8800:8800 \
  -v $(pwd)/service-account.json:/app/service-account.json \
  parlant-lifestyle-agent
```

## 🧪 Testing

Test individual tools:

```python
import asyncio
from app.tools import get_weather

async def test():
    result = await get_weather(None, "Tokyo")
    print(result.data)

asyncio.run(test())
```

## 📚 Learn More

- [Parlant Documentation](https://parlant.io/docs)
- [Parlant GitHub](https://github.com/emcie-co/parlant)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

For issues and questions:
- Check the [docs](./docs/) folder
- Visit [Parlant Discord](https://discord.gg/duxWqxKk6J)
- Open an issue on GitHub

## 🙏 Acknowledgments

- Built with [Parlant](https://github.com/emcie-co/parlant) by Emcie
- Powered by Google Vertex AI
- Weather data from wttr.in
- Recipe data from TheMealDB

---

Made with ❤️ using Parlant Framework
