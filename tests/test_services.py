import asyncio
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pyflow_ai_stack.services.base import BaseService
from pyflow_ai_stack.services.configs import (GeminiConfig, RedisConfig,
                                              S3Config)
from pyflow_ai_stack.services.gemini_service import GeminiService
from pyflow_ai_stack.services.health_service import HealthService
from pyflow_ai_stack.services.redis_service import RedisService
from pyflow_ai_stack.services.s3_service import S3Service

# --- GeminiService Upload Tests ---


@pytest.mark.asyncio
async def test_gemini_upload_file_success(gemini_config, tmp_path):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_upload = AsyncMock()
        mock_instance.aio.files.upload = mock_upload

        mock_file = MagicMock()
        mock_upload.return_value = mock_file

        service = GeminiService(gemini_config)
        temp_file = tmp_path / "test.txt"
        temp_file.write_text("hello")

        result = await service.upload_file(str(temp_file), "test.txt", "text/plain")
        assert result == mock_file
        mock_upload.assert_called_once()
        assert not os.path.exists(str(temp_file))


@pytest.mark.asyncio
async def test_gemini_upload_file_error(gemini_config, tmp_path):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_upload = AsyncMock()
        mock_instance.aio.files.upload = mock_upload
        mock_upload.side_effect = Exception("Upload fail")

        service = GeminiService(gemini_config)
        temp_file = tmp_path / "test.txt"
        temp_file.write_text("hello")

        with pytest.raises(Exception):
            await service.upload_file(str(temp_file), "test.txt")
        assert not os.path.exists(str(temp_file))


@pytest.mark.asyncio
async def test_gemini_upload_file_no_client():
    config = GeminiConfig(api_key=None)
    service = GeminiService(config)
    with pytest.raises(ValueError) as excinfo:
        await service.upload_file("path", "name")
    assert "Gemini client is not initialized" in str(excinfo.value)


# --- HealthService Tests ---


@pytest.mark.asyncio
async def test_health_service_basic():
    service = HealthService(app_name="test-app")
    result = await service.check_health(depends=0)
    assert result["status"] == "healthy"
    assert result["app"] == "test-app"
    assert "redis" not in result


@pytest.mark.asyncio
async def test_health_service_full_success():
    rs = AsyncMock()
    rs.ping.return_value = True
    gs = AsyncMock()
    gs.ping.return_value = True
    s3 = AsyncMock()
    s3.ping.return_value = True

    service = HealthService(redis_service=rs, gemini_service=gs, s3_service=s3)
    result = await service.check_health(depends=1)

    assert result["status"] == "healthy"
    assert result["redis"] == "connected"
    assert result["gemini"] == "connected"
    assert result["s3"] == "connected"


@pytest.mark.asyncio
async def test_health_service_full_failure():
    rs = AsyncMock()
    rs.ping.return_value = False
    gs = AsyncMock()
    gs.ping.return_value = False
    s3 = AsyncMock()
    s3.ping.return_value = False

    service = HealthService(redis_service=rs, gemini_service=gs, s3_service=s3)
    result = await service.check_health(depends=1)

    assert result["status"] == "unhealthy"
    assert result["redis"] == "disconnected"
    assert result["gemini"] == "disconnected"
    assert result["s3"] == "disconnected"


# --- BaseService Tests ---


@pytest.mark.asyncio
async def test_base_service_hooks():
    service = BaseService()

    # Track hook calls
    calls = []

    async def before_hook(context):
        calls.append(f"before_{context['method']}")

    def after_hook(context):
        calls.append(f"after_{context['method']}")

    service.add_hook("before", before_hook)
    service.add_hook("after", after_hook)

    async def sample_method(arg1):
        return f"result_{arg1}"

    result = await service.execute_with_hooks("sample", sample_method, "val")

    assert result == "result_val"
    assert "before_sample" in calls
    assert "after_sample" in calls


@pytest.mark.asyncio
async def test_base_service_error_hook():
    service = BaseService()
    calls = []

    async def error_hook(context):
        calls.append(f"error_{context['method']}_{type(context['error']).__name__}")

    service.add_hook("error", error_hook)

    async def failing_method():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        await service.execute_with_hooks("failing", failing_method)

    assert "error_failing_ValueError" in calls


@pytest.mark.asyncio
async def test_base_service_hook_execution_error():
    service = BaseService()

    def bad_hook(context):
        raise RuntimeError("hook failed")

    service.add_hook("before", bad_hook)

    # Should not raise exception, just log error
    await service._trigger_hooks("before", {"method": "test"})


def test_base_service_invalid_hook():
    service = BaseService()
    with pytest.raises(ValueError):
        service.add_hook("invalid", lambda x: x)


# --- GeminiService Tests ---


@pytest.fixture
def gemini_config():
    return GeminiConfig(
        api_key="test_key", model_name="gemini-pro", concurrency_limit=2
    )


@pytest.mark.asyncio
async def test_gemini_service_initialization(gemini_config):
    with patch("pyflow_ai_stack.services.gemini_service.genai.Client") as mock_client:
        service = GeminiService(gemini_config)
        assert service.client is not None
        mock_client.assert_called_once_with(api_key="test_key")


@pytest.mark.asyncio
async def test_gemini_service_initialization_no_key():
    config = GeminiConfig(api_key=None)
    service = GeminiService(config)
    assert service.client is None


@pytest.mark.asyncio
async def test_gemini_generate_content_success(gemini_config):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        # Setup the mock chain: client.aio.models.generate_content
        mock_instance = mock_client_cls.return_value
        mock_generate = AsyncMock()
        mock_instance.aio.models.generate_content = mock_generate

        mock_response = MagicMock()
        mock_response.text = "generated text"
        mock_generate.return_value = mock_response

        service = GeminiService(gemini_config)
        result = await service.generate_content("hello")

        assert result == "generated text"
        mock_generate.assert_called_once()


@pytest.mark.asyncio
async def test_gemini_generate_content_with_advanced_options(gemini_config):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_generate = AsyncMock()
        mock_instance.aio.models.generate_content = mock_generate

        mock_response = MagicMock()
        mock_response.text = "advanced result"
        mock_generate.return_value = mock_response

        service = GeminiService(gemini_config)
        result = await service.generate_content(
            "hello",
            system_instruction="You are a helpful assistant",
            generation_config={"temperature": 0.7},
        )
        assert result == "advanced result"

        # Verify call arguments
        call_kwargs = mock_generate.call_args.kwargs
        assert call_kwargs["model"] == "gemini-pro"
        assert call_kwargs["contents"] == ["hello"]
        assert call_kwargs["config"].system_instruction == "You are a helpful assistant"
        assert call_kwargs["config"].temperature == 0.7


@pytest.mark.asyncio
async def test_gemini_generate_content_no_text(gemini_config):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_generate = AsyncMock()
        mock_instance.aio.models.generate_content = mock_generate

        mock_response = MagicMock()
        mock_response.text = None
        mock_generate.return_value = mock_response

        service = GeminiService(gemini_config)
        result = await service.generate_content("hello")
        assert result == ""


@pytest.mark.asyncio
async def test_gemini_generate_content_error(gemini_config):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_generate = AsyncMock()
        mock_instance.aio.models.generate_content = mock_generate

        mock_generate.side_effect = Exception("API Error")

        service = GeminiService(gemini_config)
        with pytest.raises(Exception) as excinfo:
            await service.generate_content("hello")
        assert "API Error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_gemini_generate_content_no_model():
    config = GeminiConfig(api_key=None)
    service = GeminiService(config)
    with pytest.raises(ValueError) as excinfo:
        await service.generate_content("hello")
    assert "Gemini client is not initialized" in str(excinfo.value)


@pytest.mark.asyncio
async def test_gemini_ping_success(gemini_config):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_generate = AsyncMock()
        mock_instance.aio.models.generate_content = mock_generate

        mock_response = MagicMock()
        mock_response.text = "pong"
        mock_generate.return_value = mock_response

        service = GeminiService(gemini_config)
        assert await service.ping() is True


@pytest.mark.asyncio
async def test_gemini_ping_failure(gemini_config):
    with patch(
        "pyflow_ai_stack.services.gemini_service.genai.Client"
    ) as mock_client_cls:
        mock_instance = mock_client_cls.return_value
        mock_generate = AsyncMock()
        mock_instance.aio.models.generate_content = mock_generate

        mock_generate.side_effect = Exception("Fail")

        service = GeminiService(gemini_config)
        assert await service.ping() is False


@pytest.mark.asyncio
async def test_gemini_ping_no_model():
    config = GeminiConfig(api_key=None)
    service = GeminiService(config)
    assert await service.ping() is False


# --- RedisService Tests ---


@pytest.fixture
def redis_config():
    return RedisConfig(host="localhost", port=6379)


@pytest.mark.asyncio
async def test_redis_service_ping_success(redis_config):
    with patch("redis.asyncio.Redis.ping", new_callable=AsyncMock) as mock_ping:
        mock_ping.return_value = True
        service = RedisService(redis_config)
        result = await service.ping()
        assert result is True


@pytest.mark.asyncio
async def test_redis_service_ping_failure(redis_config):
    with patch("redis.asyncio.Redis.ping", new_callable=AsyncMock) as mock_ping:
        mock_ping.side_effect = Exception("Connection error")
        service = RedisService(redis_config)
        result = await service.ping()
        assert result is False


@pytest.mark.asyncio
async def test_redis_service_set_success(redis_config):
    with patch("redis.asyncio.Redis.set", new_callable=AsyncMock) as mock_set:
        service = RedisService(redis_config)
        await service.set("key", "value", expire=10)
        mock_set.assert_called_once_with("key", "value", ex=10)


@pytest.mark.asyncio
async def test_redis_service_set_error(redis_config):
    with patch("redis.asyncio.Redis.set", new_callable=AsyncMock) as mock_set:
        mock_set.side_effect = Exception("Set error")
        service = RedisService(redis_config)
        with pytest.raises(Exception):
            await service._set(
                "key", "value"
            )  # Test internal to check error handling before hooks if needed


@pytest.mark.asyncio
async def test_redis_service_get_success(redis_config):
    with patch("redis.asyncio.Redis.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = "value"
        service = RedisService(redis_config)
        result = await service.get("key")
        assert result == "value"


@pytest.mark.asyncio
async def test_redis_service_get_error(redis_config):
    with patch("redis.asyncio.Redis.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("Get error")
        service = RedisService(redis_config)
        with pytest.raises(Exception):
            await service.get("key")


@pytest.mark.asyncio
async def test_redis_service_delete_success(redis_config):
    with patch("redis.asyncio.Redis.delete", new_callable=AsyncMock) as mock_delete:
        service = RedisService(redis_config)
        await service.delete("key")
        mock_delete.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_redis_service_delete_error(redis_config):
    with patch("redis.asyncio.Redis.delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.side_effect = Exception("Delete error")
        service = RedisService(redis_config)
        with pytest.raises(Exception):
            await service.delete("key")


# --- S3Service Tests ---


@pytest.fixture
def s3_config():
    return S3Config(bucket_name="test-bucket")


@pytest.mark.asyncio
async def test_s3_service_upload_success(s3_config):
    service = S3Service(s3_config)
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        result = await service.upload_file("content", "key")
        assert "s3://test-bucket/key" == result
        mock_s3.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_s3_service_upload_error(s3_config):
    service = S3Service(s3_config)
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_s3.put_object.side_effect = Exception("S3 Error")
        with pytest.raises(Exception):
            await service.upload_file("content", "key")


@pytest.mark.asyncio
async def test_s3_service_get_file_success(s3_config):
    service = S3Service(s3_config)
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_body = AsyncMock()
        mock_body.read.return_value = b"file content"
        mock_s3.get_object.return_value = {"Body": mock_body}
        result = await service.get_file("key")
        assert result == "file content"


@pytest.mark.asyncio
async def test_s3_service_get_file_error(s3_config):
    service = S3Service(s3_config)
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_s3.get_object.side_effect = Exception("S3 Get Error")
        with pytest.raises(Exception):
            await service.get_file("key")


@pytest.mark.asyncio
async def test_s3_service_ping_success(s3_config):
    service = S3Service(s3_config)
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_s3.head_bucket.return_value = {}
        assert await service.ping() is True


@pytest.mark.asyncio
async def test_s3_service_ping_failure(s3_config):
    service = S3Service(s3_config)
    mock_s3 = AsyncMock()
    with patch.object(service.session, "client", return_value=mock_s3):
        mock_s3.__aenter__.return_value = mock_s3
        mock_s3.head_bucket.side_effect = Exception("Fail")
        assert await service.ping() is False
