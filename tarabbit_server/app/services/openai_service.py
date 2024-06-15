# app/services/openai_service.py

import openai
from core.config import settings
from utils.logging import get_logger
from utils.decoder import Decoder

logger = get_logger(__name__)

openai.api_key = Decoder.decrypt(settings.OPENAI_API_KEY, settings.SECRET_KEY)


def generate_fortune(prompt: str) -> str:
    logger.info("Generating fortune for prompt: %s", prompt)
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048)
        fortune = response.choices[0].message.content
        logger.info("Generated fortune: %s", fortune)
        return fortune
    except Exception as e:
        logger.error("Error generating fortune: %s", str(e))
        raise
