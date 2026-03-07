# Data Schemas (Pydantic Models)

**PyFlow AI Stack** uses Pydantic models for data validation and consistency across its API and services.

## Overview

The models are located in `pyflow_ai_stack.schemas.models` and are primarily used for:

- Structuring requests to services.
- Validating service responses.
- Handling batches of tasks and global file references.

## Core Models

### GlobalFile

Schema for a file reference shared across multiple tasks.

| Attribute | Type | Description |
| --- | --- | --- |
| `uri` | `str` | URI of the file (e.g., S3 URL). |
| `mime_type` | `str` | MIME type of the file. |

### TaskRequest

Schema for an individual task request.

| Attribute | Type | Description |
| --- | --- | --- |
| `task_id` | `str` | Unique identifier for the task. |
| `prompt` | `str` | Prompt to be processed by Gemini. |

### BatchRequest

Schema for a batch of task requests.

| Attribute | Type | Description | Default |
| --- | --- | --- | --- |
| `project_id` | `str` | Unique identifier for the project. | - |
| `mode` | `Literal["sync", "async"]` | Execution mode. | `"sync"` |
| `global_files` | `Optional[List[GlobalFile]]` | Files shared across all tasks. | `None` |
| `tasks` | `List[TaskRequest]` | List of individual tasks. | - |
| `webhook_url` | `Optional[str]` | Webhook URL for async completion notification. | `None` |

### TaskResponse

Schema for an individual task response.

| Attribute | Type | Description |
| --- | --- | --- |
| `task_id` | `str` | Unique identifier for the task. |
| `status` | `str` | Status of the task (e.g., "success", "error"). |
| `result` | `Optional[str]` | Result content from Gemini. |
| `error` | `Optional[str]` | Error message if the task failed. |

### BatchResponse

Schema for a batch response.

| Attribute | Type | Description |
| --- | --- | --- |
| `project_id` | `str` | Unique identifier for the project. |
| `results` | `List[TaskResponse]` | List of results for each task. |

### HealthResponse

Schema for the health check response.

| Attribute | Type | Description |
| --- | --- | --- |
| `status` | `str` | Overall health status ("healthy" or "unhealthy"). |
| `app` | `str` | Name of the application. |
| `redis` | `Optional[str]` | Connection status for Redis. |
| `gemini` | `Optional[str]` | Connection status for Gemini. |
| `s3` | `Optional[str]` | Connection status for S3. |
