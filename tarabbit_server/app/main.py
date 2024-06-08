# app/main.py

import asyncio
from fastapi import FastAPI

from api.endpoints import fortune, telegram, referrer
from utils.logging import get_logger
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
app.include_router(referrer.router, prefix="/referral", tags=["referral"])


async def run():
    # Run the FastAPI server
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8001, reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    logger.info("Starting application")
    asyncio.run(run())
