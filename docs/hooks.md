# Lifecycle Hooks

**PyFlow AI Stack** includes a flexible lifecycle hook system implemented in the `BaseService` class. All core services (`GeminiService`, `RedisService`, `S3Service`, `HealthService`) inherit from this base and support these hooks.

## Hook Stages

There are three main stages where you can register callbacks:

- **`before`**: Executed immediately before the core method logic.
- **`after`**: Executed after the core method logic successfully completes.
- **`error`**: Executed if an exception occurs during method execution.

## Hook Context Object

Each hook callback receives a `context` dictionary containing the following information:

| Key | Description |
| --- | --- |
| `service` | The name of the service class (e.g., `"GeminiService"`). |
| `method` | The name of the method being executed (e.g., `"generate_content"`). |
| `args` | Positional arguments passed to the method. |
| `kwargs` | Keyword arguments passed to the method. |
| `result` | The return value of the method (Available only in `after` hooks). |
| `error` | The exception object (Available only in `error` hooks). |

## Registering Hooks

You can add hooks using the `add_hook(stage, callback)` method. Callbacks can be either synchronous or asynchronous functions.

```python
async def my_before_hook(context):
    print(f"Executing {context['method']} in {context['service']}")

gemini_service.add_hook("before", my_before_hook)
```

## Example: Logging and Auditing

```python
import time

async def log_after_execution(context):
    method = context["method"]
    print(f"Successfully finished {method}")
    # You could log the result or time taken here

async def handle_error(context):
    print(f"Error in {context['method']}: {context['error']}")

# 1. Register an 'after' hook for logging
gemini_service.add_hook("after", log_after_execution)

# 2. Register an 'error' hook for custom error handling/alerting
gemini_service.add_hook("error", handle_error)

# Now, any call to gemini_service.generate_content() will trigger these hooks
await gemini_service.generate_content("Hello!")
```

## Internal Architecture

The `BaseService` handles hook execution through the `execute_with_hooks` wrapper. It ensures that hooks are triggered in the correct order and that errors within hooks themselves are caught and logged without crashing the main service call.
