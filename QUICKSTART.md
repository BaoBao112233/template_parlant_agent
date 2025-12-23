# 🚀 Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.10 or higher
- ✅ Google Cloud service account JSON file
- ✅ Docker (optional, for container deployment)

## Step 1: Get Your Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to "IAM & Admin" > "Service Accounts"
4. Create a service account with "Vertex AI User" role
5. Create and download JSON key
6. Save as `service-account.json` in project root

## Step 2: Quick Setup

### Using Setup Script (Recommended)
```bash
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings
```

## Step 3: Configure Environment

Edit `.env` file:
```env
VERTEX_AI_PROJECT_ID=your-gcp-project-id
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-2.0-flash-exp
```

## Step 4: Run the Application

### Local Development
```bash
python -m app.main
```

### Docker Deployment
```bash
docker-compose up -d
```

## Step 5: Access the Interfaces

Open your browser:
- 🌐 Web Interface: http://localhost:8000
- 🎮 Parlant Playground: http://localhost:8800
- 📚 API Documentation: http://localhost:8000/docs

## Try It Out!

Test with these example queries:
1. "What's the weather in Tokyo?"
2. "Find me recipes with chicken"
3. "Calculate BMI for 70kg and 175cm"
4. "Convert 100 USD to EUR"
5. "Flip a coin"

## Troubleshooting

### Service Account Issues
```bash
# Verify JSON is valid
python -m json.tool service-account.json

# Check permissions
gcloud projects get-iam-policy PROJECT_ID
```

### Port Conflicts
```bash
# Check what's using the port
lsof -i :8000

# Use different ports
export API_PORT=8001
export PARLANT_PORT=8801
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. Read [Full Documentation](docs/README.md)
2. Explore [API Reference](docs/API.md)
3. Check [Tools Documentation](docs/TOOLS.md)
4. Learn about [Deployment](docs/DEPLOYMENT.md)

## Getting Help

- 📖 Check the `docs/` folder
- 💬 Join [Parlant Discord](https://discord.gg/duxWqxKk6J)
- 🐛 Open an issue on GitHub

---

**Ready to build amazing AI agents!** 🎉
