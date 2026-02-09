# Service Documentation

This document describes how to use the core utility services in the boilerplate. All services now support a unified configuration system and a hook/middleware mechanism.

## Core Concepts

### 1. Configuration Objects
Services no longer read directly from environment variables. They are initialized with specific configuration objects (Pydantic models) found in `app/services/configs.py`.

### 2. Base Service & Hooks
All services inherit from `BaseService`, which provides a hook mechanism to intercept execution at three stages: `before`, `after`, and `error`.

**Example: Adding a Hook**
```python
from pyflow_ai_stack.services.redis_service import redis_service

async def log_before(context):
    print(f"Executing {context['method']} in {context['service']}")

redis_service.add_hook("before", log_before)
```

---

## 1. Gemini Service
Handles AI content generation using Google's Gemini API with advanced prompt and configuration support.

**Usage:**
```python
from pyflow_ai_stack.services.gemini_service import get_gemini_service

# Basic usage
gemini_service = get_gemini_service()
result = await gemini_service.generate_content("Your prompt here")

# Advanced usage with System Prompt and Generation Config
result = await gemini_service.generate_content(
    prompt="Tell me a joke",
    system_instruction="You are a sarcastic comedian.",
    generation_config={"temperature": 0.9, "max_output_tokens": 100}
)
```

**Key Features:**
- **System Instruction**: Support for defining the AI's persona/constraints.
- **Generation Config**: Pass parameters like `temperature`, `top_p`, etc.
- **Concurrency Control**: Uses a semaphore limited by `concurrency_limit` in its config.

---

## 2. Redis Service
Handles asynchronous caching and state management.

**Usage:**
```python
from pyflow_ai_stack.services.redis_service import redis_service

# Set a value
await redis_service.set("key", "value", expire=3600)

# Get a value
value = await redis_service.get("key")

# Delete a key
await redis_service.delete("key")
```

---

## 3. S3 Service
Handles asynchronous file storage on AWS S3 or MinIO.

**Usage:**
```python
from pyflow_ai_stack.services.s3_service import s3_service

# Upload a file
s3_uri = await s3_service.upload_file(
    content="file content", 
    s3_key="path/to/file.txt"
)

# Download a file
content = await s3_service.get_file("path/to/file.txt")
```

---

## Service Initialization (Manual)
While singletons are provided, you can instantiate services manually for testing or multi-node configurations:

```python
from pyflow_ai_stack.services.configs import RedisConfig
from pyflow_ai_stack.services.redis_service import RedisService

custom_config = RedisConfig(host="other-host", port=6379)
custom_service = RedisService(config=custom_config)
```

---

## Environment Variables
Environment variables are managed by `Pydantic Settings` in `app/core/config.py`.

### Gemini API
- `GEMINI_API_KEY`: API key.
- `GEMINI_MODEL`: Model version (default: `gemini-2.0-flash`).
- `CONCURRENCY_LIMIT`: Max concurrent requests.

### Redis
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`.

### AWS S3 / MinIO
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET_NAME`, `S3_ENDPOINT_URL`.
