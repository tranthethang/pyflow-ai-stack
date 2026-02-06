"""
Service for checking application health.

This module provides the HealthService class which aggregates health status
from various system components like Redis, Gemini, and S3.
"""

from typing import Any, Dict

from app.core.config import settings
from app.services.base import BaseService
from app.services.gemini_service import gemini_service
from app.services.redis_service import redis_service
from app.services.s3_service import s3_service


class HealthService(BaseService):
    """
    Service class for health check operations.

    Inherits from BaseService to support execution hooks.
    """

    def __init__(self):
        """Initialize HealthService."""
        super().__init__()

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
            "app": settings.APP_NAME,
        }

        if depends == 1:
            redis_status = await redis_service.ping()
            gemini_status = await gemini_service.ping()
            s3_status = await s3_service.ping()

            health_status.update(
                {
                    "redis": "connected" if redis_status else "disconnected",
                    "gemini": "connected" if gemini_status else "disconnected",
                    "s3": "connected" if s3_status else "disconnected",
                }
            )

            if not all([redis_status, gemini_status, s3_status]):
                health_status["status"] = "unhealthy"

        return health_status


# Global singleton instance
health_service = HealthService()
