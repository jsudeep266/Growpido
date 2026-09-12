import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATA_SOURCE: str = os.getenv("DATA_SOURCE", "local").lower()
    DB_PATH: str = os.getenv("DB_PATH", "growpido_track_a.db")
    
    # LLM Config: "openai" or "groq"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq").lower()
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    PROXYCURL_API_KEY: str = os.getenv("PROXYCURL_API_KEY", "")
    SLACK_REVIEWER_ID: str = os.getenv("SLACK_REVIEWER_ID", "U_LOCAL_ADMIN")

    # Default entities if none provided in UI
    TARGET_ENTITIES: list[str] = ["Growpido", "Nidhi Hooda"]
