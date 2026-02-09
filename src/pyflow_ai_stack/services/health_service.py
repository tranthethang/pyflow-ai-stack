"""
Service for checking application health.

This module provides the HealthService class which aggregates health status
from various system components like Redis, Gemini, and S3.
"""

from typing import Any, Dict, Optional

from pyflow_ai_stack.services.base import BaseService


class HealthService(BaseService):
    """
    Service class for health check operations.

    Inherits from BaseService to support execution hooks.
    """

    def __init__(
        self,
        redis_service=None,
        gemini_service=None,
        s3_service=None,
        app_name: str = "pyflow-ai-stack",
    ):
        """
        Initialize HealthService.

        Args:
            redis_service: Redis service instance.
            gemini_service: Gemini service instance.
            s3_service: S3 service instance.
            app_name: Name of the application.
        """
        super().__init__()
        self._redis_service = redis_service
        self._gemini_service = gemini_service
        self._s3_service = s3_service
        self._app_name = app_name

    async def check_health(self, depends: int = 0) -> Dict[str, Any]:
        """
        Check the health of the application and its dependencies.

        Args:
            depends (int): Whether to check external dependencies.
                           If 1, check dependencies; otherwise, only check app status.

        Returns:
            dict: A dictionary containing the health status.
        """
        return await self.execute_with_hooks(
            "check_health", self._check_health, depends
        )

    async def _check_health(self, depends: int = 0) -> Dict[str, Any]:
        """Internal method to check health."""
        health_status = {
            "status": "healthy",
            "app": self._app_name,
        }

        if depends == 1:
            # Use provided services
            rs = self._redis_service
            gs = self._gemini_service
            s3 = self._s3_service

            results = {}
            all_connected = True

            if rs:
                redis_status = await rs.ping()
                results["redis"] = "connected" if redis_status else "disconnected"
                if not redis_status:
                    all_connected = False

            if gs:
                gemini_status = await gs.ping()
                results["gemini"] = "connected" if gemini_status else "disconnected"
                if not gemini_status:
                    all_connected = False

            if s3:
                s3_status = await s3.ping()
                results["s3"] = "connected" if s3_status else "disconnected"
                if not s3_status:
                    all_connected = False

            health_status.update(results)

            if not all_connected:
                health_status["status"] = "unhealthy"

        return health_status
