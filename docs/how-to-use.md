# Service Documentation

This document describes how to use the core utility services in the `pyflow-ai-stack` library. All services follow a unified configuration system and a hook mechanism for intercepting execution.

---

## Core Concepts

### 1. Configuration System
The library uses `Pydantic Settings` for centralized configuration. You can load settings from environment variables, a `.env` file, or pass them directly.

```python
from pyflow_ai_stack import Settings

# Default loading (Environment Variables -> .env -> defaults)
settings = Settings()

# Load from specific .env file
# settings = Settings.load(env_file=".env.prod")

# Access specific service configuration models
gemini_cfg = settings.gemini
redis_cfg = settings.redis
s3_cfg = settings.s3
```

### 2. Base Service & Hooks
All services (Gemini, Redis, S3, Health) inherit from `BaseService`. This provides a hook mechanism to intercept execution at three stages: `before`, `after`, and `error`.

**Example: Adding a Hook**
```python
from pyflow_ai_stack import RedisService, Settings

settings = Settings()
redis_service = RedisService(settings.redis)

async def log_before(context):
    print(f"Executing {context['method']} in {context['service']}")

redis_service.add_hook("before", log_before)
```

---

## 1. Gemini Service
Handles AI content generation using Google's Gemini API with managed concurrency.

**Usage:**
```python
from pyflow_ai_stack import GeminiService, Settings

settings = Settings()
gemini_service = GeminiService(settings.gemini)

# Basic generation
result = await gemini_service.generate_content("Your prompt here")

# Advanced usage with System Instruction
result = await gemini_service.generate_content(
    prompt="Tell me a joke",
    system_instruction="You are a sarcastic comedian.",
    generation_config={"temperature": 0.9}
)

# File upload to Gemini
file_obj = await gemini_service.upload_file(
    temp_path="path/to/local/image.jpg",
    filename="image.jpg",
    mime_type="image/jpeg"
)
```

**Key Features:**
- **System Instruction**: Define the AI's persona or constraints.
- **Concurrency Control**: Automatically managed via a semaphore based on `CONCURRENCY_LIMIT`.
- **Hooks**: Intercept generation or upload calls for logging or auditing.

---

## 2. Redis Service
Handles asynchronous caching and state management using `redis-py`.

**Usage:**
```python
from pyflow_ai_stack import RedisService, Settings

settings = Settings()
redis = RedisService(settings.redis)

# Set a value with 1-hour expiration
await redis.set("user_session:123", "session_data", expire=3600)

# Get a value
value = await redis.get("user_session:123")

# Delete a key
await redis.delete("user_session:123")
```

---

## 3. S3 Service
Handles asynchronous file storage on AWS S3 or MinIO using `aioboto3`.

**Usage:**
```python
from pyflow_ai_stack import S3Service, Settings

settings = Settings()
s3 = S3Service(settings.s3)

# Upload content (string or bytes)
s3_uri = await s3.upload_file(
    content="file content", 
    s3_key="documents/report.txt",
    content_type="text/plain"
)

# Download content as bytes
content_bytes = await s3.get_file("documents/report.txt")
```

---

## 4. Health Service
Aggregates health status from all connected services.

**Usage:**
```python
from pyflow_ai_stack import HealthService, GeminiService, RedisService, S3Service, Settings

settings = Settings()

# Initialize dependencies
redis_svc = RedisService(settings.redis)
gemini_svc = GeminiService(settings.gemini)
s3_svc = S3Service(settings.s3)

# Initialize Health Service
health = HealthService(
    redis_service=redis_svc,
    gemini_service=gemini_svc,
    s3_service=s3_svc,
    app_name="my-api-service"
)

# Deep health check (checks external dependencies)
status = await health.check_health(depends=True)
```

---

## Environment Variables

Settings are automatically loaded from these environment variables:

### Gemini
- `GEMINI_API_KEY`: Google AI API Key (also supports `GOOGLE_API_KEY`).
- `GEMINI_MODEL`: Model version (default: `gemini-2.0-flash`).
- `CONCURRENCY_LIMIT`: Max concurrent requests (default: `5`).

### Redis
- `REDIS_HOST`: Redis host (default: `localhost`).
- `REDIS_PORT`: Redis port (default: `6379`).
- `REDIS_PASSWORD`: Optional password.
- `REDIS_DB`: Database index (default: `0`).

### S3 / Storage
- `AWS_ACCESS_KEY_ID`: AWS Access Key.
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Key.
- `AWS_REGION`: AWS Region (default: `ap-southeast-1`).
- `S3_BUCKET_NAME`: Target bucket.
- `S3_ENDPOINT_URL`: Custom endpoint for MinIO/other S3 providers.
