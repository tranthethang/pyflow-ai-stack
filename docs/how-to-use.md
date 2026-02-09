# Service Documentation

This document describes how to use the core utility services in the `pyflow-ai-stack` library. All services now support a unified configuration system and a hook mechanism for intercepting execution.

---

## Core Concepts

### 1. Configuration System
The library uses `Pydantic Settings` for centralized configuration. You can load settings from environment variables, a `.env` file, or pass them directly.

```python
from pyflow_ai_stack import Settings

# Default loading (ENV -> .env -> defaults)
settings = Settings()

# Access specific service configs
gemini_cfg = settings.gemini
redis_cfg = settings.redis
s3_cfg = settings.s3
```

### 2. Base Service & Hooks
All services (Gemini, Redis, S3) inherit from `BaseService`. This provides a hook mechanism to intercept execution at three stages: `before`, `after`, and `error`.

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

# Advanced usage with System Prompt
result = await gemini_service.generate_content(
    prompt="Tell me a joke",
    system_instruction="You are a sarcastic comedian.",
    generation_config={"temperature": 0.9}
)
```

**Key Features:**
- **System Instruction**: Define the AI's persona or constraints.
- **Concurrency Control**: Automatically managed via a semaphore based on `CONCURRENCY_LIMIT`.
- **Hooks**: Intercept generation calls for logging or auditing.

---

## 2. Redis Service
Handles asynchronous caching and state management.

**Usage:**
```python
from pyflow_ai_stack import RedisService, Settings

settings = Settings()
redis = RedisService(settings.redis)

# Set a value
await redis.set("key", "value", expire=3600)

# Get a value
value = await redis.get("key")

# Delete a key
await redis.delete("key")
```

---

## 3. S3 Service
Handles asynchronous file storage on AWS S3 or MinIO.

**Usage:**
```python
from pyflow_ai_stack import S3Service, Settings

settings = Settings()
s3 = S3Service(settings.s3)

# Upload a file
s3_uri = await s3.upload_file(
    content="file content", 
    s3_key="path/to/file.txt",
    content_type="text/plain"
)

# Download a file
content = await s3.get_file("path/to/file.txt")
```

---

## 4. Health Service
Aggregates health status from all connected services.

**Usage:**
```python
from pyflow_ai_stack import HealthService, GeminiService, RedisService, S3Service, Settings

settings = Settings()
health = HealthService(
    gemini=GeminiService(settings.gemini),
    redis=RedisService(settings.redis),
    s3=S3Service(settings.s3)
)

# Deep health check
status = await health.check_health(depends=1)
```

---

## Environment Variables

Settings are automatically loaded from these environment variables:

### Gemini
- `GEMINI_API_KEY`: Google AI API Key.
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
