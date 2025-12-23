"""Vertex AI configuration and client setup."""
import os
from typing import Optional
from google.auth import default
from google.oauth2 import service_account
import vertexai
from app.config.settings import settings


def initialize_vertex_ai() -> None:
    """Initialize Vertex AI with service account credentials."""
    
    # Set the service account key path
    if settings.SERVICE_ACCOUNT_PATH.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(settings.SERVICE_ACCOUNT_PATH)
        
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            str(settings.SERVICE_ACCOUNT_PATH),
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        # Extract project ID from service account if not set
        if not settings.VERTEX_AI_PROJECT_ID:
            with open(settings.SERVICE_ACCOUNT_PATH, 'r') as f:
                import json
                service_account_info = json.load(f)
                project_id = service_account_info.get('project_id', '')
                settings.VERTEX_AI_PROJECT_ID = project_id
        
        # Initialize Vertex AI
        vertexai.init(
            project=settings.VERTEX_AI_PROJECT_ID,
            location=settings.VERTEX_AI_LOCATION,
            credentials=credentials
        )
        
        print(f"✅ Vertex AI initialized with project: {settings.VERTEX_AI_PROJECT_ID}")
    else:
        raise FileNotFoundError(
            f"Service account file not found at {settings.SERVICE_ACCOUNT_PATH}. "
            "Please ensure service-account.json exists in the project root."
        )


def get_vertex_ai_model_name() -> str:
    """Get the Vertex AI model name."""
    return settings.VERTEX_AI_MODEL
