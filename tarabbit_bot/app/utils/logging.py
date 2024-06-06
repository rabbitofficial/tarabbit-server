# app/utils/logging.py

import logging
import sys

# Define the format for log messages
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create and configure the root logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format=LOG_FORMAT,  # Set the format for log messages
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to the console
        logging.FileHandler("app.log", mode='a')  # Log to a file (append mode)
    ]
)


# Function to get a configured logger
def get_logger(name):
    return logging.getLogger(name)
