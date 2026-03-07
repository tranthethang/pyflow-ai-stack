# Health Check Service

**HealthService** provides an interface for checking the status of your application and its core dependencies (Redis, Gemini, and S3).

## Initialization

Initialize the service by injecting instances of other services:

```python
from pyflow_ai_stack.services.health_service import HealthService

health_service = HealthService(
    redis_service=redis_service,
    gemini_service=gemini_service,
    s3_service=s3_service,
    app_name="my-custom-app"
)
```

## Methods

### `check_health`

Aggregates health status information into a single dictionary.

- **`depends`** (`bool`, default: `False`): Whether to check external dependencies.
  - If `False`: Only checks if the application is "healthy".
  - If `True`: Attempts to `ping` each injected service to determine connection status.

**Returns**: `dict` (containing health details).

## Health Status Response

The returned dictionary follows this structure (see [**HealthResponse**](../schemas.md)):

```json
{
    "status": "healthy",
    "app": "my-custom-app",
    "redis": "connected",
    "gemini": "connected",
    "s3": "connected"
}
```

If any checked dependency is unreachable, the overall `status` will be set to `"unhealthy"`.

## Example: Application Health Endpoint

```python
@app.get("/health")
async def health_check():
    # Only check basic app health
    return await health_service.check_health(depends=False)

@app.get("/health/deep")
async def deep_health_check():
    # Check all external dependencies
    return await health_service.check_health(depends=True)
```
