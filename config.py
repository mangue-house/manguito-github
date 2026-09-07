import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Config(BaseModel):
    github_token: str = Field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    github_org: str = Field(default_factory=lambda: os.getenv("GITHUB_ORG", "MangueHouse"))
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    discord_webhook_url: str = Field(default_factory=lambda: os.getenv("DISCORD_WEBHOOK_URL", ""))

def get_config() -> Config:
    config = Config()
    missing = []
    if not config.github_token:
        missing.append("GITHUB_TOKEN")
    if not config.gemini_api_key:
        missing.append("GEMINI_API_KEY")
    if not config.discord_webhook_url:
        missing.append("DISCORD_WEBHOOK_URL")

    if missing:
        raise ValueError(f"❌ Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing)}")

    return config
