# PyFlow AI Stack

**PyFlow AI Stack** is a high-performance Python library designed for building robust **Node APIs** and **AI Workers** within workflow automation systems. It provides a unified interface for interacting with **Google Gemini AI**, **Redis Caching**, and **S3-compatible Object Storage**.

## Features

- **Google Gemini AI**: Seamless integration with the Gemini model for content generation and file processing.
- **Redis Caching**: Efficient asynchronous caching with support for expiration and connection management.
- **S3 Storage**: Asynchronous access to S3-compatible storage (e.g., AWS S3, MinIO).
- **Health Checks**: Built-in service health monitoring for API endpoints.
- **Lifecycle Hooks**: Flexible `before`, `after`, and `error` hooks for all service operations.
- **Pydantic Validation**: Strong typing and data validation for all requests and responses.

## Installation

You can install the library using `pip`:

```bash
pip install pyflow-ai-stack
```

For development purposes, install it with development dependencies:

```bash
git clone https://github.com/pyflow-ai-stack/pyflow-ai-stack.git
cd pyflow-ai-stack
pip install -e .[dev]
```

## Quick Start

Here is a basic example of how to use `GeminiService` and `RedisService`:

```python
import asyncio
import os
from pyflow_ai_stack.services.configs import GeminiConfig, RedisConfig
from pyflow_ai_stack.services.gemini_service import GeminiService
from pyflow_ai_stack.services.redis_service import RedisService

async def main():
    # 1. Initialize Gemini Service
    gemini_config = GeminiConfig(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash"
    )
    gemini_service = GeminiService(gemini_config)
    
    # 2. Generate Content
    response = await gemini_service.generate_content("Hello, Gemini!")
    print(f"Gemini: {response}")

    # 3. Initialize Redis Service
    redis_config = RedisConfig(host="localhost", port=6379)
    redis_service = RedisService(redis_config)
    
    # 4. Use Caching
    await redis_service.set("greeting", "Hello from Redis!", expire=60)
    cached_val = await redis_service.get("greeting")
    print(f"Redis: {cached_val}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

- [**Configuration**](./configuration.md): Environment variables and settings.
- [**Services**](./services/index.md): Detailed documentation for each service.
- [**Schemas**](./schemas.md): Data validation models.
- [**Hooks**](./hooks.md): Lifecycle hooks system.
