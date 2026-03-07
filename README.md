# PyFlow AI Stack

**PyFlow AI Stack** is a high-performance Python library designed for building robust **Node APIs** and **AI Workers** within workflow automation systems (like **Dify**, LangChain, or custom microservices).

It provides a unified, production-ready interface for interacting with **Google Gemini AI**, **Redis Caching**, and **S3-compatible Object Storage**, featuring built-in concurrency management, health diagnostics, and structured configuration.

---

## ✨ Key Features

- **Unified AI Interface**: Seamlessly interact with Google Gemini models with managed concurrency.
- **Asynchronous Caching**: Optimized Redis service for high-throughput data persistence and retrieval.
- **Scalable Storage**: Multi-cloud support for AWS S3, MinIO, and other S3-compatible providers.
- **Production Ready**: Built-in logging, error handling, and health check diagnostics.
- **Base Service & Hooks**: Intercept execution at `before`, `after`, and `error` stages for all services.

---

## 🛠️ Installation

You can install the library directly from [PyPI](https://pypi.org/project/pyflow-ai-stack/):

```bash
pip install pyflow-ai-stack==1.0.0
```

Alternatively, install from the repository:

```bash
pip install git+https://github.com/tranthethang/pyflow-ai-stack.git
```

---

## 🧠 Core Concepts

### 1. Configuration System
The library uses `Pydantic Settings` for centralized configuration. It is designed to be **stateless**: by default, it loads settings from **environment variables** or direct initialization.

#### Note on `.env` Files:
- **Core Library**: Does **not** automatically load a `.env` file to maintain flexibility and avoid side effects.
- **Examples & Development**: You can use `Settings.load(env_file=".env")` to load configurations from a file, which is how the provided `examples/` are configured.

```python
from pyflow_ai_stack import Settings

# 1. Default (Loads from Environment Variables only)
settings = Settings()

# 2. Manual loading (Loads from .env file + Environment Variables)
settings = Settings.load(env_file=".env")

# 3. Direct access to service configs
gemini_cfg = settings.gemini
```

### 2. Base Service & Hooks
All services (Gemini, Redis, S3) inherit from `BaseService`, providing a hook mechanism to intercept execution.

```python
from pyflow_ai_stack import RedisService, Settings

settings = Settings()
redis_service = RedisService(settings.redis)

async def log_before(context):
    print(f"Executing {context['method']} in {context['service']}")

redis_service.add_hook("before", log_before)
```

---

## 🚀 Service Usage

### 1. Gemini Service
Handles AI content generation using Google's Gemini API with managed concurrency.

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

### 2. Redis Service
Handles asynchronous caching and state management.

```python
from pyflow_ai_stack import RedisService, Settings

settings = Settings()
redis = RedisService(settings.redis)

# Set a value
await redis.set("key", "value", expire=3600)

# Get a value
value = await redis.get("key")
```

### 3. S3 Service
Handles asynchronous file storage on AWS S3 or MinIO.

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
```

### 4. Health Service
Aggregates health status from all connected services.

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

## ⚙️ Environment Variables

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

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
