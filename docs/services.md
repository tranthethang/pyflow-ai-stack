# Service Documentation

This document describes how to use the core utility services in the boilerplate.

## 1. Gemini Service
Handles AI content generation using Google's Gemini API with built-in concurrency control.

**Usage:**
```python
from app.services.gemini_service import gemini_service

# Basic usage
result = await gemini_service.generate_content("Your prompt here")

# Advanced usage with multiple parts (e.g., text and file data)
result = await gemini_service.generate_content(
    prompt="Describe this content",
    parts=[{"text": "Context info"}]
)
```

**Key Features:**
- **Concurrency Control**: Uses a semaphore limited by `CONCURRENCY_LIMIT` to prevent rate limiting.
- **Model Configuration**: Defaults to `gemini-2.0-flash`.

## 2. Redis Service
Handles asynchronous caching and state management using `redis-py` (asyncio).

**Usage:**
```python
from app.services.redis_service import redis_service

# Set a value with optional expiration (in seconds)
await redis_service.set("key", "value", expire=3600)

# Get a value
value = await redis_service.get("key")

# Delete a key
await redis_service.delete("key")

# Check connectivity
is_alive = await redis_service.ping()
```

## 3. S3 Service
Handles asynchronous file storage on AWS S3 or MinIO using `aioboto3`.

**Usage:**
```python
from app.services.s3_service import s3_service

# Upload a file (defaults to text/plain)
s3_uri = await s3_service.upload_file(
    content="file content", 
    s3_key="path/to/file.txt",
    content_type="text/plain"
)

# Download and decode file content
content = await s3_service.get_file("path/to/file.txt")
```

## Environment Variables
Ensure these are set in your `.env` file:

### General
- `APP_NAME`: Name of the application.
- `DEBUG`: Enable debug mode (`True`/`False`).
- `CONCURRENCY_LIMIT`: Maximum concurrent requests for services (default: `5`).

### Gemini API
- `GEMINI_API_KEY`: Your Google Gemini API key (Required).
- `GEMINI_MODEL`: Gemini model version (default: `gemini-2.0-flash`).

### Redis
- `REDIS_HOST`: Redis server host (default: `localhost`).
- `REDIS_PORT`: Redis server port (default: `6379`).
- `REDIS_PASSWORD`: Redis password (optional).
- `REDIS_DB`: Redis database index (default: `0`).

### AWS S3 / MinIO
- `AWS_ACCESS_KEY_ID`: AWS Access Key ID.
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Access Key.
- `AWS_REGION`: AWS region (default: `ap-southeast-1`).
- `S3_BUCKET_NAME`: Name of the S3 bucket.
- `S3_ENDPOINT_URL`: Custom S3 endpoint URL (Required for MinIO).
