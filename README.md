# Parlant Lifestyle Agent

🤖 An AI-powered lifestyle assistant built with [Parlant](https://github.com/emcie-co/parlant) framework, featuring 10+ tools powered by Google Vertex AI Gemini 2.0 Flash.

## ✨ Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd template_parlant_agent

# Install dependencies
pip install -r requirements.txt

# Configure (add your service-account.json and edit .env)
cp .env.example .env

# Run
python -m app.main
```

Visit:
- 🌐 Web UI: http://localhost:8000
- 🎮 Parlant Playground: http://localhost:8800
- 📚 API Docs: http://localhost:8000/docs

## 🚀 Docker Deployment

```bash
docker-compose up -d
```

## 🛠️ Features

- **10+ Lifestyle Tools**: Weather, recipes, fitness, currency, and more
- **Vertex AI Gemini**: Powered by Google's latest AI model
- **FastAPI Backend**: Modern async Python API
- **Web Interface**: Beautiful, responsive UI
- **Docker Ready**: Easy deployment

## 📖 Documentation

See the `docs/` folder for comprehensive documentation:
- [README.md](docs/README.md) - Full documentation
- [API.md](docs/API.md) - API reference
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide

## 🧰 Available Tools

1. 🌤️ Weather Forecast
2. 🍳 Recipe Search
3. 💪 Fitness Calculators
4. 💱 Currency Converter
5. 🕐 Date/Time Utilities
6. 🌍 Translation
7. 🎲 Random Tools
8. 📰 News Headlines
9. ✨ Daily Quotes
10. And more!

## 📋 Prerequisites

- Python 3.10+
- Google Cloud service account with Vertex AI
- Docker (optional)

## 🤝 Contributing

Contributions welcome! See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for guidelines.

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE)

## 🙏 Acknowledgments

Built with [Parlant](https://github.com/emcie-co/parlant) by Emcie

---

Made with ❤️ using Parlant Framework
