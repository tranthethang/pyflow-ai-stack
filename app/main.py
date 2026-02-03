"""
Main application module for the FastAPI boilerplate.

This module initializes the FastAPI application, registers API routes,
and defines basic health check endpoints.
"""

import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints import router as v1_router
from app.core.config import Config
from app.core.logger import logger
from app.schemas.models import HealthResponse

app = FastAPI(
    title=Config.APP_NAME,
    description="Boilerplate for FastAPI with Gemini, Redis, and S3",
    version="1.0.0",
)

# Register routers
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])


@app.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def health_check(depends: int = 0):
    """
    Check the health of the application and its dependencies.

    Args:
        depends (int): Whether to check external dependencies (Redis, Gemini, S3).
                       If 1, check dependencies; otherwise, only check app status.

    Returns:
        dict: A dictionary containing the health status of the application and its dependencies.
    """
    from app.services.gemini_service import gemini_service
    from app.services.redis_service import redis_service
    from app.services.s3_service import s3_service

    health_status = {
        "status": "healthy",
        "app": Config.APP_NAME,
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
    else:
        # Default behavior: only check redis or just return healthy
        # User asked: (mặc định là 0: thì không check redis, gemini, s3)
        pass

    return health_status


if __name__ == "__main__":
    logger.info(f"Starting {Config.APP_NAME} on port: {Config.APP_PORT}")
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=Config.APP_PORT, reload=Config.DEBUG
    )
