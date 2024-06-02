# app/main.py

import asyncio
from fastapi import FastAPI

from app.api.endpoints import fortune, telegram
from app.services.telegram_service import start_bot_polling
from app.utils.logging import get_logger
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Get a logger instance for this module
logger = get_logger(__name__)

# Include the routers for API endpoints
app.include_router(fortune.router, prefix="/fortune", tags=["fortune"])
app.include_router(telegram.router, prefix="/telegram", tags=["telegram"])


async def start_bot():
    await start_bot_polling()


async def run():
    # Create a task for the bot and run the FastAPI server
    bot_task = asyncio.create_task(start_bot())
    # Run the FastAPI server
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8001, reload=True)
    server = uvicorn.Server(config)
    await asyncio.gather(server.serve(), bot_task)


if __name__ == "__main__":
    logger.info("Starting application")
    asyncio.run(run())
