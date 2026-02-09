# PyFlow AI Stack

**PyFlow AI Stack** is a high-performance Python library designed for building robust **Node APIs** and **AI Workers** within workflow automation systems (like **Dify**, LangChain, or custom microservices).

It provides a unified, production-ready interface for interacting with **Google Gemini AI**, **Redis Caching**, and **S3-compatible Object Storage**, featuring built-in concurrency management, health diagnostics, and structured configuration.

---

## ✨ Key Features

- **Unified AI Interface**: Seamlessly interact with Google Gemini models with managed concurrency.
- **Asynchronous Caching**: Optimized Redis service for high-throughput data persistence and retrieval.
- **Scalable Storage**: Multi-cloud support for AWS S3, MinIO, and other S3-compatible providers.
- **Production Ready**: Built-in logging, error handling, and health check diagnostics.
- **Workflow Native**: Specifically architected to act as a backend for workflow nodes and microservice workers.

---

## 🛠️ Installation

You can install the library directly from the repository:

```bash
pip install git+https://github.com/tranthethang/pyflow-ai-stack.git
```

Or if you are developing locally:

```bash
git clone https://github.com/tranthethang/pyflow-ai-stack.git
cd pyflow-ai-stack
pip install .
```

---

## 🚀 Quick Start

### 1. Configuration

The library uses a centralized `Settings` class powered by Pydantic. You can configure it via environment variables or a `.env` file.

```python
from pyflow_ai_stack import Settings

# Load settings from environment/defaults
settings = Settings()

# Or load from a specific .env file
settings = Settings.load(env_file=".env")
```

### 2. Using Gemini AI

Handle complex LLM tasks with the `GeminiService`.

```python
import asyncio
from pyflow_ai_stack import GeminiService, Settings

async def main():
    settings = Settings()
    service = GeminiService(settings.gemini)
    
    # Generate simple text
    response = await service.generate_content("Explain quantum computing in 50 words.")
    print(f"Gemini: {response}")

    # Generate with system instructions
    response = await service.generate_content(
        prompt="Tell me a joke.",
        system_instruction="You are a sarcastic comedian."
    )
    print(f"Sarcastic Gemini: {response}")

asyncio.run(main())
```

### 3. Asynchronous Caching with Redis

```python
import asyncio
from pyflow_ai_stack import RedisService, Settings

async def cache_example():
    settings = Settings()
    redis = RedisService(settings.redis)
    
    # Set a value with 60s expiration
    await redis.set("user_session_123", '{"name": "John"}', expire=60)
    
    # Get a value
    data = await redis.get("user_session_123")
    print(f"Cached Data: {data}")

asyncio.run(cache_example())
```

### 4. S3 Object Storage

```python
import asyncio
from pyflow_ai_stack import S3Service, Settings

async def s3_example():
    settings = Settings()
    s3 = S3Service(settings.s3)
    
    # Upload content
    uri = await s3.upload_file(
        content="Hello S3!",
        s3_key="notes/hello.txt",
        content_type="text/plain"
    )
    print(f"Uploaded to: {uri}")
    
    # Download content
    content = await s3.get_file("notes/hello.txt")
    print(f"Downloaded: {content}")

asyncio.run(s3_example())
```

---

## 📂 Library Components

| Component | Description |
| :--- | :--- |
| `GeminiService` | Handles interactions with Google Generative AI (Gemini). |
| `RedisService` | Asynchronous Redis client for caching and state management. |
| `S3Service` | Asynchronous S3 client for object storage (AWS, MinIO, etc.). |
| `HealthService` | Aggregates health status from all connected services. |
| `Settings` | Pydantic-based configuration management. |

---

## 🏥 Health Diagnostics

Ensure all your services are correctly configured and reachable:

```python
import asyncio
from pyflow_ai_stack import HealthService, Settings, GeminiService, RedisService, S3Service

async def check_system():
    settings = Settings()
    
    # Pass service instances to HealthService
    health = HealthService(
        gemini=GeminiService(settings.gemini),
        redis=RedisService(settings.redis),
        s3=S3Service(settings.s3)
    )
    
    status = await health.check_health(depends=1)
    print(f"System Status: {status}")

asyncio.run(check_system())
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
