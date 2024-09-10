# mypy: ignore_errors
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "staging"
    mongo_uri: str
    mongo_db: str
    graph_url: str = "https://graph.facebook.com/v17.0"
    graph_token: str
    page_name: str

    bing_url: str = "https://api.bing.microsoft.com/v7.0"
    bing_token: str

    class Config:
        env_file = ".env"


settings = Settings()
