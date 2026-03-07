# Configuration

**PyFlow AI Stack** uses `pydantic-settings` to manage configuration through environment variables and optional `.env` files.

## Settings Class

The `Settings` class is the central point for all library configurations. It can be loaded directly from environment variables or a specific `.env` file.

```python
from pyflow_ai_stack.core.config import Settings

# 1. Load from environment variables
settings = Settings()

# 2. Load from a specific .env file
settings = Settings.load(env_file=".env.dev")
```

## Environment Variables Mapping

The following table summarizes the environment variables supported by the library:

| Environment Variable | Description | Default Value |
| --- | --- | --- |
| `GEMINI_API_KEY` | Google Gemini API Key. Also supports `GOOGLE_API_KEY`. | `None` |
| `GEMINI_MODEL` | Gemini model name to use. | `gemini-2.0-flash` |
| `CONCURRENCY_LIMIT` | Maximum number of concurrent Gemini requests. | `5` |
| `AWS_ACCESS_KEY_ID` | Access key for AWS or S3-compatible storage. | `None` |
| `AWS_SECRET_ACCESS_KEY` | Secret access key for S3. | `None` |
| `AWS_REGION` | AWS region name. | `ap-southeast-1` |
| `S3_BUCKET_NAME` | Default bucket name for S3 operations. | `None` |
| `S3_ENDPOINT_URL` | Custom endpoint URL for S3 (e.g., for MinIO). | `None` |
| `REDIS_HOST` | Redis server hostname. | `localhost` |
| `REDIS_PORT` | Redis server port. | `6379` |
| `REDIS_PASSWORD` | Password for Redis server. | `None` |
| `REDIS_DB` | Redis database number. | `0` |

## Per-Service Configuration Models

The `Settings` class provides properties to easily retrieve configuration for individual services as separate Pydantic models:

- `settings.gemini`: Returns a `GeminiConfig` instance.
- `settings.redis`: Returns a `RedisConfig` instance.
- `settings.s3`: Returns an `S3Config` instance.

### Example: Manual Configuration

You can also initialize service-specific configuration models manually:

```python
from pyflow_ai_stack.services.configs import GeminiConfig

gemini_config = GeminiConfig(
    api_key="your_api_key_here",
    model_name="gemini-2.0-flash",
    concurrency_limit=10
)
```
