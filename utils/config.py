from pathlib import Path
import os
from typing import Dict, Any, Optional
import streamlit as st

from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    STREAMLIT_PORT: int = 8501
    STREAMLIT_HOST: str = "0.0.0.0"
    TAX_THRESHOLD: int = 183
    FIREBASE_SERVICE_ACCOUNT: str = ""
    FIREBASE_CONFIG: str = ""
    GMAIL_CREDENTIALS_FILE: str = ""
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    SENTRY_DSN: str = ""
    DAILY_REMINDER_TIME: str = "09:00"
    NOTIFICATION_EMAIL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()