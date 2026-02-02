from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.gemini_service import GeminiService
from app.services.redis_service import RedisService
from app.services.s3_service import S3Service

# --- GeminiService Tests ---


@pytest.mark.asyncio
async def test_gemini_service_initialization():
    with patch("app.core.config.Config.GEMINI_API_KEY", "test_key"):
        service = GeminiService()
        assert service.model is not None


@pytest.mark.asyncio
async def test_gemini_service_initialization_no_key():
    with patch("app.core.config.Config.GEMINI_API_KEY", None):
        service = GeminiService()
        assert service.model is None


@pytest.mark.asyncio
async def test_gemini_generate_content_success():
    with patch("app.core.config.Config.GEMINI_API_KEY", "test_key"):
        service = GeminiService()
        mock_response = MagicMock()
        mock_response.text = "generated text"

        # Mock run_in_executor
        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(
                return_value=mock_response
            )
            result = await service.generate_content("hello")
            assert result == "generated text"


@pytest.mark.asyncio
async def test_gemini_generate_content_with_parts():
    with patch("app.core.config.Config.GEMINI_API_KEY", "test_key"):
        service = GeminiService()
        mock_response = MagicMock()
        mock_response.text = "generated text"
        parts = [{"file_data": {"mime_type": "text/plain", "file_uri": "uri"}}]

        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(
                return_value=mock_response
            )
            result = await service.generate_content("hello", parts=parts)
            assert result == "generated text"
            # Verify that the lambda passed to run_in_executor calls generate_content with combined parts
            # We can't easily check the lambda content, but we cover the line.


@pytest.mark.asyncio
async def test_gemini_generate_content_no_text():
    with patch("app.core.config.Config.GEMINI_API_KEY", "test_key"):
        service = GeminiService()
        mock_response = MagicMock()
        mock_response.text = None

        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(
                return_value=mock_response
            )
            result = await service.generate_content("hello")
            assert result == ""


@pytest.mark.asyncio
async def test_gemini_generate_content_error():
    with patch("app.core.config.Config.GEMINI_API_KEY", "test_key"):
        service = GeminiService()
        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_in_executor = AsyncMock(
                side_effect=Exception("API Error")
            )
            with pytest.raises(Exception) as excinfo:
                await service.generate_content("hello")
            assert "API Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_gemini_generate_content_no_model():
    with patch("app.core.config.Config.GEMINI_API_KEY", None):
        service = GeminiService()
        with pytest.raises(ValueError) as excinfo:
            await service.generate_content("hello")
        assert "Gemini model is not initialized" in str(excinfo.value)


# --- RedisService Tests ---


@pytest.mark.asyncio
async def test_redis_service_ping_success():
    with patch("redis.asyncio.Redis.ping", new_callable=AsyncMock) as mock_ping:
        mock_ping.return_value = True
        service = RedisService()
        result = await service.ping()
        assert result is True


@pytest.mark.asyncio
async def test_redis_service_ping_failure():
    with patch("redis.asyncio.Redis.ping", new_callable=AsyncMock) as mock_ping:
        mock_ping.side_effect = Exception("Connection error")
        service = RedisService()
        result = await service.ping()
        assert result is False


@pytest.mark.asyncio
async def test_redis_service_set_success():
    with patch("redis.asyncio.Redis.set", new_callable=AsyncMock) as mock_set:
        service = RedisService()
        await service.set("key", "value", expire=10)
        mock_set.assert_called_once_with("key", "value", ex=10)


@pytest.mark.asyncio
async def test_redis_service_set_error():
    with patch("redis.asyncio.Redis.set", new_callable=AsyncMock) as mock_set:
        mock_set.side_effect = Exception("Set error")
        service = RedisService()
        with pytest.raises(Exception):
            await service.set("key", "value")


@pytest.mark.asyncio
async def test_redis_service_get_success():
    with patch("redis.asyncio.Redis.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = "value"
        service = RedisService()
        result = await service.get("key")
        assert result == "value"
        mock_get.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_redis_service_get_error():
    with patch("redis.asyncio.Redis.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("Get error")
        service = RedisService()
        with pytest.raises(Exception):
            await service.get("key")


@pytest.mark.asyncio
async def test_redis_service_delete_success():
    with patch("redis.asyncio.Redis.delete", new_callable=AsyncMock) as mock_delete:
        service = RedisService()
        await service.delete("key")
        mock_delete.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_redis_service_delete_error():
    with patch("redis.asyncio.Redis.delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.side_effect = Exception("Delete error")
        service = RedisService()
        with pytest.raises(Exception):
            await service.delete("key")


# --- S3Service Tests ---


@pytest.mark.asyncio
async def test_s3_service_upload_success():
    service = S3Service()
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        result = await service.upload_file("content", "key")
        assert "s3://" in result
        mock_s3.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_s3_service_upload_error():
    service = S3Service()
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_s3.put_object.side_effect = Exception("S3 Error")
        with pytest.raises(Exception):
            await service.upload_file("content", "key")


@pytest.mark.asyncio
async def test_s3_service_get_file_success():
    service = S3Service()
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3

        mock_body = AsyncMock()
        mock_body.read.return_value = b"file content"
        mock_s3.get_object.return_value = {"Body": mock_body}

        result = await service.get_file("key")
        assert result == "file content"


@pytest.mark.asyncio
async def test_s3_service_get_file_error():
    service = S3Service()
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_s3.get_object.side_effect = Exception("S3 Get Error")
        with pytest.raises(Exception):
            await service.get_file("key")
