# app/services/telegram_service.py

import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from core.config import settings
from utils.logging import get_logger

logger = get_logger(__name__)

bot = Bot(token=settings.TELEGRAM_TOKEN)


def start(update, context):
    user = update.effective_user
    username = user.username if user.username else user.first_name
    updated_message = f"Hello, {username}! {settings.WELCOME_MESSAGE}"
    web_app_url = "https://t.me/Tarabbit_bot/myapp"
    play_button = InlineKeyboardButton("Play \u25B6", url=web_app_url)
    keyboard = InlineKeyboardMarkup([[play_button]])
    context.bot.send_message(chat_id=update.effective_chat.id, text=updated_message, reply_markup=keyboard)


async def start_bot_polling():
    queue = asyncio.Queue()
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    updater.start_polling()
    logger.info("Telegram bot polling started")

    try:
        while True:
            await asyncio.sleep(600)
            logger.info("Polling is ongoing...")
    except asyncio.CancelledError:
        logger.info("Polling has been cancelled")
    finally:
        updater.stop()
        logger.info("Telegram bot polling stopped")