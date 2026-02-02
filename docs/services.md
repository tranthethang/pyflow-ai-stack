# Service Documentation

This document describes how to use the core utility services in the boilerplate.

## 1. Gemini Service
Handles AI content generation using Google's Gemini API.

**Usage:**
```python
from app.services.gemini_service import gemini_service

result = await gemini_service.generate_content("Your prompt here")
```

## 2. Redis Service
Handles caching and state management.

**Usage:**
```python
from app.services.redis_service import redis_service

await redis_service.set("key", "value", expire=3600)
value = await redis_service.get("key")
```

## 3. S3 Service
Handles file storage on AWS S3 or MinIO.

**Usage:**
```python
from app.services.s3_service import s3_service

s3_uri = await s3_service.upload_file("file content", "path/to/file.txt")
content = await s3_service.get_file("path/to/file.txt")
```

## Environment Variables
Ensure these are set in your `.env` file:
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `REDIS_HOST`, `REDIS_PORT`: Redis connection details.
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET_NAME`: S3 credentials.
