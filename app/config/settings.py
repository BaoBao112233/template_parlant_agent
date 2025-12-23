"""Configuration settings for the Parlant agent."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    SERVICE_ACCOUNT_PATH: Path = PROJECT_ROOT / "service-account.json"
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "Parlant Lifestyle Agent"
    API_VERSION: str = "1.0.0"
    
    # Parlant settings
    PARLANT_HOST: str = "0.0.0.0"
    PARLANT_PORT: int = 8800
    
    # Vertex AI settings
    VERTEX_AI_PROJECT_ID: str = ""
    VERTEX_AI_LOCATION: str = "us-central1"
    VERTEX_AI_MODEL: str = "gemini-2.0-flash-exp"
    
    # Agent settings
    AGENT_NAME: str = "LifestyleAssistant"
    AGENT_DESCRIPTION: str = "A helpful lifestyle assistant with various daily life tools"
    
    # External API keys (optional for tools)
    WEATHER_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None
    EXCHANGE_RATE_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
