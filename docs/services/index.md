# Services Overview

**PyFlow AI Stack** provides a set of core services designed to handle common tasks in AI-driven workflow automation. All services follow a consistent architecture, providing:

- **Asynchronous Operations**: All methods are designed to be used with `async`/`await`.
- **Lifecycle Hooks**: Every service inherits from `BaseService`, which allows you to register `before`, `after`, and `error` hooks.
- **Dependency Injection**: Services are easily composed and can be used independently or together (e.g., in `HealthService`).

## Available Services

| Service | Description | Documentation |
| --- | --- | --- |
| `GeminiService` | Integration with Google Gemini AI for content generation and file uploads. | [**Gemini**](./gemini.md) |
| `RedisService` | Asynchronous Redis client for caching and data storage. | [**Redis**](./redis.md) |
| `S3Service` | Asynchronous S3-compatible storage (AWS S3, MinIO, etc.). | [**S3 Storage**](./s3.md) |
| `HealthService` | Aggregates health status for the application and its dependencies. | [**Health Check**](./health.md) |

## Common Usage Pattern

Typically, you initialize a service with its configuration model:

```python
from pyflow_ai_stack.services.configs import RedisConfig
from pyflow_ai_stack.services.redis_service import RedisService

# 1. Configuration
config = RedisConfig(host="localhost", port=6379)

# 2. Service Initialization
redis_service = RedisService(config)

# 3. Use methods with async/await
await redis_service.set("key", "value")
```
