from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Flash Me Up Backend"
    DATABASE_URL: str = "sqlite:///./flashmeup.db"
    GROQ_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
