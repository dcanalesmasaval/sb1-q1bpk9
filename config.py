from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    default_model: str = "gpt-4-0125-preview"
    default_assistant_id: str

    class Config:
        env_file = ".env"

settings = Settings()