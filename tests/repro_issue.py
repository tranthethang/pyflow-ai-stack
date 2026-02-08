import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.configs import GeminiConfig
from app.services.gemini_service import GeminiService


@pytest.mark.asyncio
async def test_gemini_upload_file_signature():
    """
    Test that upload_file calls the SDK with the correct parameters.
    The goal is to verify if 'file' should be used instead of 'path'.
    """
    config = GeminiConfig(api_key="test_key", model_name="gemini-2.0-flash")
    service = GeminiService(config)

    # Mock the client and aio.files.upload
    mock_client = MagicMock()
    mock_upload = AsyncMock()
    mock_client.aio.files.upload = mock_upload
    service.client = mock_client

    # We want to see if this fails or if we can detect the expected parameter name
    # In some versions of google-genai, it might be 'file' or 'path'
    # The user's IDE alert suggests a mismatch.

    temp_path = "test.txt"
    with open(temp_path, "w") as f:
        f.write("test")

    try:
        await service.upload_file(temp_path, "test.txt", "text/plain")

        # Check how it was called
        args, kwargs = mock_upload.call_args
        print(f"Upload called with kwargs: {kwargs.keys()}")

        # If it was called with 'file', the fix is verified
        assert "file" in kwargs
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@pytest.mark.asyncio
async def test_gemini_service_initialization_with_settings():
    """
    Verify that get_gemini_service() initializes correctly.
    """
    from app.core.config import settings
    from app.services.gemini_service import get_gemini_service

    service = get_gemini_service()
    assert service.config.api_key == settings.GEMINI_API_KEY
    if settings.GEMINI_API_KEY:
        assert service.client is not None
