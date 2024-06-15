# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENCRYPTED_API_KEY: str = os.getenv("ENCRYPTED_API_KEY")
    MONGO_URI: str = os.getenv("MONGO_URI")


settings = Settings()
