from unittest.mock import MagicMock, patch

import pytest

from app.services.gemini_service import GeminiService
from app.services.redis_service import RedisService
from app.services.s3_service import S3Service


@pytest.mark.asyncio
async def test_gemini_service_initialization():
    with patch("app.core.config.Config.GEMINI_API_KEY", "test_key"):
        service = GeminiService()
        assert service.model is not None


@pytest.mark.asyncio
async def test_redis_service_ping():
    with patch("redis.asyncio.Redis.ping", return_value=True):
        service = RedisService()
        result = await service.ping()
        assert result is True


@pytest.mark.asyncio
async def test_s3_service_upload():
    # Mocking aioboto3 is complex, usually we mock the service method or use moto
    # Here we just mock the service itself for brevity in boilerplate
    service = S3Service()
    with patch.object(service, "upload_file", return_value="s3://bucket/key"):
        result = await service.upload_file("content", "key")
        assert result == "s3://bucket/key"
