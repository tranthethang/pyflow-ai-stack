import asyncio
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from pyflow_ai_stack.services.configs import GeminiConfig, RedisConfig
from pyflow_ai_stack.services.gemini_service import GeminiService
from pyflow_ai_stack.services.redis_service import RedisService


async def main():
    # Example Gemini usage
    gemini_config = GeminiConfig(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        concurrency_limit=5,
    )

    if gemini_config.api_key:
        gemini_service = GeminiService(gemini_config)
        print("--- Gemini Example ---")
        try:
            response = await gemini_service.generate_content(
                "Say hello in a creative way!"
            )
            print(f"Response: {response}")
        except Exception as e:
            print(f"Gemini error: {e}")
    else:
        print("GEMINI_API_KEY not found in environment.")

    # Example Redis usage
    redis_config = RedisConfig(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        password=os.getenv("REDIS_PASSWORD"),
    )

    redis_service = RedisService(redis_config)
    print("\n--- Redis Example ---")
    try:
        await redis_service.set("test_key", "Hello from PyFlow AI Stack!", expire=60)
        value = await redis_service.get("test_key")
        print(f"Stored value: {value}")
    except Exception as e:
        print(f"Redis error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
