from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_MODEL: str = "gpt-4o-mini"

settings = Settings()