# app/services/telegram_service.py

import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

bot = Bot(token=settings.TELEGRAM_TOKEN)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=settings.WELCOME_MESSAGE)
    play_button = InlineKeyboardButton("Play \u25B6", callback_data='play')
    keyboard = InlineKeyboardMarkup([[play_button]])
    context.bot.send_message(chat_id=update.effective_chat.id, text=settings.WELCOME_MESSAGE, reply_markup=keyboard)


def handle_play_button(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Play button pressed!")


async def start_bot_polling():
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    start_handler = CommandHandler('start', start)
    play_button_handler = CallbackQueryHandler(handle_play_button, pattern='play')
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(play_button_handler)

    updater.start_polling()
    logger.info("Telegram bot polling started")

    # Using asyncio to keep the bot running
    while True:
        await asyncio.sleep(3600)
