"""
Service for interacting with Google Gemini AI.

This module provides the GeminiService class which handles requests to Gemini models,
manages concurrency, and integrates with the BaseService hook system.
"""

import asyncio
import os
from typing import Any, Dict, List, Optional, cast

from google import genai
from google.genai import types

from pyflow_ai_stack.core.logger import logger
from pyflow_ai_stack.services.base import BaseService
from pyflow_ai_stack.services.configs import GeminiConfig


class GeminiService(BaseService):
    """
    Service class for Google Gemini operations.

    Inherits from BaseService to support execution hooks.
    """

    def __init__(self, config: GeminiConfig):
        """
        Initialize GeminiService with configuration.

        Args:
            config (GeminiConfig): Configuration settings for Gemini.
        """
        super().__init__()
        self.config = config
        if config.api_key:
            self.client = genai.Client(api_key=config.api_key.strip())
            self.semaphore = asyncio.Semaphore(config.concurrency_limit)
        else:
            self.client = None
            logger.warning("GEMINI_API_KEY not set. GeminiService will not function.")

    async def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        generation_config: Optional[Any] = None,
        parts: Optional[List[Any]] = None,
    ) -> str:
        """
        Generate content using Gemini, wrapped with service hooks.

        Args:
            prompt (str): The main prompt text.
            system_instruction (str, optional): Instructions for the system role.
            generation_config (dict, optional): Gemini generation configuration.
            parts (list, optional): Additional content parts (e.g., images).

        Returns:
            str: Generated text response.
        """
        return await self.execute_with_hooks(
            "generate_content",
            self._generate_content,
            prompt,
            system_instruction,
            generation_config,
            parts,
        )

    async def _generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        generation_config: Optional[Any] = None,
        parts: Optional[List[Any]] = None,
    ) -> str:
        """Internal method to call Gemini API."""
        if not self.client:
            raise ValueError("Gemini client is not initialized. Check GEMINI_API_KEY.")

        async with self.semaphore:
            try:
                # Create a new list to avoid side effects if 'parts' is passed by reference
                content_parts = (parts or []) + [prompt]

                # Configure generation settings
                config_params = {}
                if system_instruction:
                    config_params["system_instruction"] = system_instruction

                if generation_config:
                    if isinstance(generation_config, dict):
                        config_params.update(generation_config)
                    # We assume generation_config is a dictionary compatible with GenerateContentConfig

                response = await self.client.aio.models.generate_content(
                    model=self.config.model_name,
                    contents=content_parts,
                    config=(
                        types.GenerateContentConfig(**config_params)
                        if config_params
                        else None
                    ),
                )

                if not response or not response.text:
                    return ""

                return response.text
            except Exception as e:
                logger.error(f"Gemini error: {str(e)}")
                raise e

    async def upload_file(
        self, temp_path: str, filename: str, mime_type: str = None
    ) -> Any:
        """
        Upload a file to Gemini, wrapped with service hooks.

        Args:
            temp_path (str): Path to the temporary file.
            filename (str): Display name for the file.
            mime_type (str, optional): MIME type of the file.

        Returns:
            Any: The uploaded Gemini file object.
        """
        return await self.execute_with_hooks(
            "upload_file",
            self._upload_file,
            temp_path,
            filename,
            mime_type,
        )

    async def _upload_file(
        self, temp_path: str, filename: str, mime_type: str = None
    ) -> Any:
        """Internal method to upload file to Gemini."""
        if not self.client:
            raise ValueError("Gemini client is not initialized. Check GEMINI_API_KEY.")

        async with self.semaphore:
            try:
                logger.info(f"Uploading file to Gemini: {filename}")

                upload_config = None
                if filename or mime_type:
                    upload_config = types.UploadFileConfig(
                        display_name=filename, mime_type=mime_type
                    )

                gemini_file = await self.client.aio.files.upload(
                    file=temp_path, config=upload_config
                )
                return gemini_file
            except Exception as e:
                logger.error(f"Gemini upload error: {str(e)}")
                raise e
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    async def ping(self) -> bool:
        """
        Check if the Gemini service is healthy and responsive.

        Returns:
            bool: True if healthy, False otherwise.
        """
        try:
            if not self.client:
                return False
            # Check if we can access the model metadata (no tokens consumed)
            await self.client.aio.models.get(model=self.config.model_name)
            return True
        except Exception as e:
            logger.error(f"Gemini ping error: {str(e)}")
            return False


# Maintain backward compatibility but encourage get_gemini_service()
# We'll initialize it lazily when accessed if possible, but for now just provide the function
