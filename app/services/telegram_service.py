# app/services/telegram_service.py

from telegram import Bot
from config import settings

bot = Bot(token=settings.TELEGRAM_TOKEN)


def start_bot_polling():
    from telegram.ext import Updater
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    updater.start_polling()
    updater.idle()
