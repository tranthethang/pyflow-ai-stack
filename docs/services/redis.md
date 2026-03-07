# Redis Service

**RedisService** provides an asynchronous interface for key-value storage and caching using `redis-py`. It handles connection management and integrates with the library's hook system.

## Initialization

Initialize the service with a `RedisConfig` object:

```python
from pyflow_ai_stack.services.configs import RedisConfig
from pyflow_ai_stack.services.redis_service import RedisService

config = RedisConfig(
    host="localhost",
    port=6379,
    password="your_password",
    db=0,
    decode_responses=True
)
redis_service = RedisService(config)
```

## Methods

### `set`

Stores a value in Redis with an optional expiration time.

- **`key`** (`str`): The key under which the value should be stored.
- **`value`** (`str`): The string value to store.
- **`expire`** (`int`, optional): Time in seconds after which the key should expire.

### `get`

Retrieves a value from Redis by its key.

- **`key`** (`str`): The key of the value to retrieve.

**Returns**: `str` (The stored value, or `None` if the key is not found).

### `delete`

Removes a key and its associated value from Redis.

- **`key`** (`str`): The key to delete.

### `ping`

Checks if the Redis server is responsive.

**Returns**: `bool` (`True` if the server responds, `False` otherwise).

### `close`

Closes the asynchronous Redis connection pool.

## Example: Caching a Result

```python
cache_key = "api_response_123"

# Check cache
cached_result = await redis_service.get(cache_key)

if cached_result:
    print(f"Cache hit: {cached_result}")
else:
    # Perform expensive operation
    result = "Expensive API result"
    
    # Store in cache with 1-hour expiration
    await redis_service.set(cache_key, result, expire=3600)
    print(f"Cache miss, stored: {result}")
```
