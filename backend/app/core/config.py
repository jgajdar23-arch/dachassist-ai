from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # App
    app_name: str = "DachAssist AI"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
