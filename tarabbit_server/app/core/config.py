# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENCRYPTED_API_KEY: str = os.getenv("ENCRYPTED_API_KEY")
    MONGO_URI: str = os.getenv("MONGO_URI")


settings = Settings()

class PointRule:
    INVITE_NORMAL_USER = 2000
    INVITE_PREMIUM_USER = 10000
    FOLLOW_X = 5000
    FOLLOW_COMMUNITY = 10000
    INVITE_5_USER = 20000
    INVITE_20_USER = 40000
    INVITE_100_USER = 60000
    ALLOW_UP_THAN_5_LEVEL_USER_NUM = 99999
    LEVEL_DEFINE = [21000, 18000, 16000, 11000, 1000, 0]

point_rule = PointRule()
