"""
Configuration settings for NeuroTask backend
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"sqlite:///{BASE_DIR}/neurotask.db"
)

# API
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"

# NLP
NLP_MODEL = os.getenv("NLP_MODEL", "en_core_web_sm")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.6))

# Timezone
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Notifications
NOTIFICATION_CHECK_INTERVAL = int(os.getenv("NOTIFICATION_CHECK_INTERVAL", 60))

# AI/LLM (Optional)
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "False") == "True"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
