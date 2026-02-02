import redis.asyncio as redis

from app.core.config import Config
from app.core.logger import logger


class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            db=Config.REDIS_DB,
            decode_responses=True,
        )

    async def set(self, key: str, value: str, expire: int = None):
        try:
            await self.client.set(key, value, ex=expire)
        except Exception as e:
            logger.error(f"Redis set error: {str(e)}")
            raise e

    async def get(self, key: str) -> str:
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis get error: {str(e)}")
            raise e

    async def delete(self, key: str):
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {str(e)}")
            raise e

    async def ping(self) -> bool:
        try:
            return await self.client.ping()
        except Exception as e:
            logger.error(f"Redis ping error: {str(e)}")
            return False


redis_service = RedisService()
