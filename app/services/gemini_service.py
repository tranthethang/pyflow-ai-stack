import asyncio

import google.generativeai as genai

from app.core.config import Config
from app.core.logger import logger


class GeminiService:
    def __init__(self):
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            self.semaphore = asyncio.Semaphore(Config.CONCURRENCY_LIMIT)
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not set. GeminiService will not function.")

    async def generate_content(self, prompt: str, parts: list = None) -> str:
        if not self.model:
            raise ValueError("Gemini model is not initialized. Check GEMINI_API_KEY.")

        async with self.semaphore:
            try:
                # content_parts can be a list of strings or dicts (for file_data)
                content_parts = parts if parts is not None else []
                content_parts.append(prompt)

                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, lambda: self.model.generate_content(content_parts)
                )

                if not response or not response.text:
                    return ""

                return response.text
            except Exception as e:
                logger.error(f"Gemini error: {str(e)}")
                raise e

    async def ping(self) -> bool:
        try:
            if not self.model:
                return False
            # Simple check to see if the service is responsive
            await self.generate_content("ping")
            return True
        except Exception as e:
            logger.error(f"Gemini ping error: {str(e)}")
            return False


gemini_service = GeminiService()
