# app/main.py

from fastapi import FastAPI
from app.api.endpoints import fortune, telegram
from app.services.telegram_service import start_bot_polling
from app.utils.logging import get_logger

# Initialize the FastAPI app
app = FastAPI()

# Get a logger instance for this module
logger = get_logger(__name__)

# Include the routers for API endpoints
app.include_router(fortune.router, prefix="/fortune", tags=["fortune"])
app.include_router(telegram.router, prefix="/telegram", tags=["telegram"])


# Define a startup event to run the Telegram bot polling in a separate thread
@app.on_event("startup")
async def startup_event():
    import threading
    thread = threading.Thread(target=start_bot_polling)
    thread.start()
    logger.info("Telegram bot polling started")


# Run the application with Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting FastAPI application")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
