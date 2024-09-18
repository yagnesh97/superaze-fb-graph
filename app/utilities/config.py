# mypy: ignore_errors
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "staging"
    mongo_uri: str
    mongo_db: str

    graph_url: str = "https://graph.facebook.com/v20.0"
    graph_token: str
    page_id: int

    bing_url: str = "https://api.bing.microsoft.com/v7.0"
    bing_token: str

    genai_model: str = "gemini-1.5-flash"
    genai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
