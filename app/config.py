import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL")
    bot_token: str = os.getenv("BOT_TOKEN")
    debug_type: bool = True

settings = Settings()