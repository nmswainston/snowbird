
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    STREAMLIT_PORT: int = 8501
    STREAMLIT_HOST: str = "0.0.0.0"
    # add more keys as needed (e.g. PLAID_CLIENT_ID, EMAIL_SMTP)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
