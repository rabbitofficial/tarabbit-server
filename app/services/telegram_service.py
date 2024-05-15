# app/services/telegram_service.py

from telegram import Bot
from config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

bot = Bot(token=settings.TELEGRAM_TOKEN)

def start_bot_polling():
    from telegram.ext import Updater
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    updater.start_polling()
    updater.idle()
    logger.info("Telegram bot polling started")
