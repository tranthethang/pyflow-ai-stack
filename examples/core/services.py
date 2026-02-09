from typing import Optional

from examples.core.config import get_settings
from pyflow_ai_stack.services.gemini_service import GeminiService
from pyflow_ai_stack.services.health_service import HealthService
from pyflow_ai_stack.services.redis_service import RedisService
from pyflow_ai_stack.services.s3_service import S3Service

# Global service instances
_gemini_service: Optional[GeminiService] = None
_redis_service: Optional[RedisService] = None
_s3_service: Optional[S3Service] = None
_health_service: Optional[HealthService] = None


def get_gemini_service() -> GeminiService:
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService(get_settings().gemini)
    return _gemini_service


def get_redis_service() -> RedisService:
    global _redis_service
    if _redis_service is None:
        _redis_service = RedisService(get_settings().redis)
    return _redis_service


def get_s3_service() -> S3Service:
    global _s3_service
    if _s3_service is None:
        _s3_service = S3Service(get_settings().s3)
    return _s3_service


def get_health_service() -> HealthService:
    global _health_service
    if _health_service is None:
        settings = get_settings()
        _health_service = HealthService(
            redis_service=get_redis_service(),
            gemini_service=get_gemini_service(),
            s3_service=get_s3_service(),
            app_name=settings.APP_NAME,
        )
    return _health_service
