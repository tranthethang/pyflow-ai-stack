"""
Main application module for the FastAPI boilerplate.

This module initializes the FastAPI application, registers API routes,
and defines basic health check endpoints.
"""

import uvicorn
from fastapi import FastAPI

from examples.api.v1.endpoints import router as v1_router
from examples.core.config import get_settings
from examples.core.logger import logger
from examples.core.services import get_health_service
from pyflow_ai_stack.schemas.models import HealthResponse

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Boilerplate for FastAPI with Gemini, Redis, and S3",
    version="1.0.0",
)

# Register routers
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])


@app.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def health_check(depends: bool = False):
    """
    Check the health of the application and its dependencies.

    Args:
        depends (bool): Whether to check external dependencies (Redis, Gemini, S3).
                       If True, check dependencies; otherwise, only check app status.

    Returns:
        dict: A dictionary containing the health status of the application and its dependencies.
    """
    return await get_health_service().check_health(depends)


if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} on port: {settings.APP_PORT}")
    uvicorn.run(
        "examples.web_api_usage:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.DEBUG,
    )
