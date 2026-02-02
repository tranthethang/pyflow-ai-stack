import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints import router as v1_router
from app.core.config import Config
from app.core.logger import logger

app = FastAPI(
    title=Config.APP_NAME,
    description="Boilerplate for FastAPI with Gemini, Redis, and S3",
    version="1.0.0",
)

# Register routers
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])


@app.get("/health")
async def health_check():
    from app.services.redis_service import redis_service

    redis_status = await redis_service.ping()

    return {
        "status": "healthy",
        "app": Config.APP_NAME,
        "redis": "connected" if redis_status else "disconnected",
    }


if __name__ == "__main__":
    logger.info(f"Starting {Config.APP_NAME} on port: {Config.APP_PORT}")
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=Config.APP_PORT, reload=Config.DEBUG
    )
