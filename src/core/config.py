from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()