# config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")


settings = Settings()
