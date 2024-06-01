# config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    WELCOME_MESSAGE: str = os.getenv("WELCOME_MESSAGE")
    MONGO_URI: str = os.getenv("MONGO_URI")

settings = Settings()
