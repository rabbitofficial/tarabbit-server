# config.py

import os
import json
from dotenv import load_dotenv

load_dotenv()

config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')

with open(config_file_path) as config_file:
    configs = json.load(config_file)


class Settings:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    WELCOME_MESSAGE: str = configs["welcome_message"]


settings = Settings()
