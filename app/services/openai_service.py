# app/services/openai_service.py

import openai
from config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

openai.api_key = settings.OPENAI_API_KEY


def generate_fortune(prompt: str) -> str:
    logger.info("Generating fortune for prompt: %s", prompt)
    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
        fortune = response.choices[0].text.strip()
        logger.info("Generated fortune: %s", fortune)
        return fortune
    except Exception as e:
        logger.error("Error generating fortune: %s", str(e))
        raise
