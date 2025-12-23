# Development Guide

## Getting Started

This guide will help you set up your development environment and understand the project structure for contributing to the Parlant Lifestyle Agent.

## Development Environment Setup

### Prerequisites

- Python 3.10+
- Git
- Docker (optional, for testing deployments)
- VS Code or PyCharm (recommended IDEs)
- Google Cloud account with Vertex AI access

### Initial Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd template_parlant_agent
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install development dependencies**:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

4. **Setup pre-commit hooks** (optional but recommended):
```bash
pip install pre-commit
pre-commit install
```

5. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your development settings
```

## Project Architecture

### Directory Structure

```
app/
├── config/          # Configuration management
│   ├── settings.py  # Environment settings
│   └── vertex_ai.py # Vertex AI setup
├── tools/           # Parlant tools
│   ├── weather_tool.py
│   ├── recipe_tool.py
│   └── ...
├── agent.py         # Agent initialization
└── main.py          # FastAPI application

docs/                # Documentation
static/              # Static web files
service-account.json # GCP credentials
```

### Key Components

#### 1. Settings (`app/config/settings.py`)

Manages all configuration using Pydantic Settings:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    # ... more settings
```

#### 2. Vertex AI Configuration (`app/config/vertex_ai.py`)

Handles Google Cloud authentication and Vertex AI initialization:
```python
def initialize_vertex_ai():
    # Load service account
    # Initialize Vertex AI client
    # Configure Gemini model
```

#### 3. Tools (`app/tools/`)

Each tool is a Python module with async functions decorated with `@p.tool`:
```python
@p.tool
async def tool_name(context: p.ToolContext, param: str) -> p.ToolResult:
    # Tool implementation
    return p.ToolResult("Result text")
```

#### 4. Agent (`app/agent.py`)

Configures the Parlant agent with guidelines and tools:
```python
await agent.create_guideline(
    condition="When user asks X",
    action="Do Y",
    tools=[tool_function]
)
```

#### 5. FastAPI App (`app/main.py`)

REST API endpoints for interacting with the agent.

## Creating a New Tool

### Step 1: Create Tool File

Create `app/tools/your_tool.py`:

```python
"""Your tool description."""
import parlant.sdk as p


@p.tool
async def your_tool_function(
    context: p.ToolContext,
    param1: str,
    param2: int = 10
) -> p.ToolResult:
    """
    Tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (optional)
        
    Returns:
        Result description
    """
    try:
        # Your implementation here
        result = f"Processed {param1} with {param2}"
        
        return p.ToolResult(result)
    except Exception as e:
        return p.ToolResult(f"❌ Error: {str(e)}")
```

### Step 2: Export Tool

Add to `app/tools/__init__.py`:

```python
from app.tools.your_tool import your_tool_function

__all__ = [
    # ... existing tools
    "your_tool_function",
]
```

### Step 3: Register in Agent

Add to `app/agent.py`:

```python
from app.tools import your_tool_function

async def _setup_guidelines(self):
    # ... existing guidelines
    
    await self.agent.create_guideline(
        condition="User wants to use your feature",
        action="Use your_tool_function to process the request",
        tools=[your_tool_function]
    )
```

### Step 4: Test Your Tool

```python
import asyncio
from app.tools import your_tool_function
import parlant.sdk as p

async def test():
    result = await your_tool_function(
        context=None,  # Can be None for testing
        param1="test",
        param2=5
    )
    print(result.data)

asyncio.run(test())
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files, add features, fix bugs.

### 3. Test Locally

```bash
# Run the application
python -m app.main

# Test in browser
open http://localhost:8000

# Test Parlant playground
open http://localhost:8800
```

### 4. Code Quality

```bash
# Format code with black
black app/

# Sort imports
isort app/

# Lint with flake8
flake8 app/

# Type check with mypy
mypy app/
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

## Testing

### Unit Tests

Create `tests/test_tools.py`:

```python
import pytest
from app.tools import get_weather

@pytest.mark.asyncio
async def test_weather_tool():
    result = await get_weather(None, "Tokyo")
    assert "Weather in Tokyo" in result.data
    assert "Temperature" in result.data
```

Run tests:
```bash
pytest tests/
pytest --cov=app tests/  # With coverage
```

### Integration Tests

Test the full agent:

```python
import pytest
from app.agent import get_agent

@pytest.mark.asyncio
async def test_agent_weather_query():
    agent = await get_agent()
    # Test agent interaction
    assert agent.name == "LifestyleAssistant"
```

### API Tests

Test FastAPI endpoints:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_agent_info():
    response = client.get("/api/agent/info")
    assert response.status_code == 200
    assert "name" in response.json()
```

## Debugging

### Debug Mode

Set debug logging in `.env`:
```env
LOG_LEVEL=DEBUG
```

Or in code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### VS Code Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": false
    }
  ]
}
```

### Debugging Tools

Use Python debugger:
```python
import pdb; pdb.set_trace()  # Breakpoint

# Or with ipdb
import ipdb; ipdb.set_trace()
```

## Best Practices

### Code Style

1. **Follow PEP 8**: Python style guide
2. **Use type hints**: For better code clarity
3. **Write docstrings**: For all functions and classes
4. **Keep functions small**: Single responsibility principle

### Tool Development

1. **Error Handling**: Always wrap in try-except
2. **User-Friendly Messages**: Use emojis and clear text
3. **Validation**: Validate input parameters
4. **Async/Await**: Use async functions for I/O operations

Example:
```python
@p.tool
async def example_tool(context: p.ToolContext, value: int) -> p.ToolResult:
    """Tool with best practices."""
    # Validate input
    if value < 0:
        return p.ToolResult("❌ Value must be positive")
    
    try:
        # Async operation
        async with aiohttp.ClientSession() as session:
            async with session.get(f"api.example.com/{value}") as response:
                data = await response.json()
        
        # Format result nicely
        result = f"✅ Success: {data['result']}"
        return p.ToolResult(result)
        
    except Exception as e:
        # User-friendly error
        return p.ToolResult(f"❌ Error: {str(e)}")
```

### Agent Guidelines

1. **Clear Conditions**: Be specific about when guidelines apply
2. **Actionable Actions**: Clearly state what the agent should do
3. **Appropriate Tools**: Only include necessary tools
4. **Test Guidelines**: Verify they work as expected

### API Development

1. **RESTful Design**: Follow REST principles
2. **Validation**: Use Pydantic models
3. **Error Responses**: Return appropriate HTTP status codes
4. **Documentation**: Use OpenAPI/Swagger annotations

## Performance Optimization

### Async Operations

Use async/await for I/O operations:
```python
# Good
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()

# Avoid blocking calls
import time
time.sleep(1)  # Don't do this!
```

### Caching

Implement caching for expensive operations:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_function(param):
    # Computation here
    return result
```

### Connection Pooling

Reuse HTTP sessions:
```python
# Create session once
session = aiohttp.ClientSession()

# Reuse for multiple requests
async with session.get(url1) as resp1:
    data1 = await resp1.json()

async with session.get(url2) as resp2:
    data2 = await resp2.json()

# Close when done
await session.close()
```

## Environment Variables

### Development (.env)
```env
# Development settings
API_HOST=127.0.0.1
API_PORT=8000
PARLANT_PORT=8800
LOG_LEVEL=DEBUG

# Test mode flags
TESTING=true
USE_MOCK_APIS=true
```

### Production
```env
# Production settings
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
TESTING=false
```

## Documentation

### Code Documentation

Use docstrings for all public functions:
```python
def function_name(param1: str, param2: int) -> str:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        
    Example:
        >>> function_name("test", 5)
        "result"
    """
```

### API Documentation

FastAPI generates docs automatically, but you can enhance:
```python
@app.post(
    "/api/chat",
    response_model=ChatResponse,
    summary="Chat with agent",
    description="Send a message and receive response",
    tags=["chat"]
)
async def chat(message: ChatMessage):
    """Detailed endpoint description."""
    pass
```

## Troubleshooting Development Issues

### Import Errors

```bash
# Ensure app is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Or use pip install in editable mode
pip install -e .
```

### Vertex AI Errors

```bash
# Verify credentials
gcloud auth application-default login

# Check service account
gcloud auth list

# Test API access
gcloud ai models list --region=us-central1
```

### Port Conflicts

```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

## Resources

- [Parlant Documentation](https://parlant.io/docs)
- [Parlant Examples](https://github.com/emcie-co/parlant/tree/main/examples)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [aiohttp Docs](https://docs.aiohttp.org/)
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)

## Getting Help

- Open an issue on GitHub
- Join [Parlant Discord](https://discord.gg/duxWqxKk6J)
- Check existing documentation in `docs/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

Follow the code style and include documentation for new features.

---

Happy coding! 🚀
