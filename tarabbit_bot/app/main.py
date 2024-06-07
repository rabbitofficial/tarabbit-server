import asyncio
from services.telegram_service import start_bot_polling

async def start_bot():
    await start_bot_polling()
    
if __name__ == "__main__":
    asyncio.run(start_bot())