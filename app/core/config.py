import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.getenv("APP_NAME", "fastapi-boilerplate")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    APP_PORT = int(os.getenv("APP_PORT", 80))

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

    # Concurrency Control
    CONCURRENCY_LIMIT = int(os.getenv("CONCURRENCY_LIMIT", 5))
