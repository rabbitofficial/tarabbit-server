# app/services/telegram_service.py

import asyncio
from telegram import Bot
from telegram.ext import Updater
from config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

bot = Bot(token=settings.TELEGRAM_TOKEN)


async def start_bot_polling():
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    updater.start_polling()
    logger.info("Telegram bot polling started")
    # Using asyncio to keep the bot running
    while True:
        await asyncio.sleep(3600)
