# app/main.py

import asyncio
from fastapi import FastAPI
from app.api.endpoints import fortune, telegram
from app.services.telegram_service import start_bot_polling
from app.utils.logging import get_logger
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# Get a logger instance for this module
logger = get_logger(__name__)

# Include the routers for API endpoints
app.include_router(fortune.router, prefix="/fortune", tags=["fortune"])
app.include_router(telegram.router, prefix="/telegram", tags=["telegram"])


async def start_bot():
    await start_bot_polling()


def run_uvicorn():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    logger.info("Starting application")

    # Create the asyncio event loop
    loop = asyncio.get_event_loop()

    # Schedule the Telegram bot polling in the background
    loop.create_task(start_bot())

    # Run the Uvicorn server in the foreground
    loop.run_in_executor(None, run_uvicorn)

    # Run the event loop
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
