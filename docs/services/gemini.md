# Gemini Service

**GeminiService** provides a high-level asynchronous interface for interacting with Google Gemini AI models. It handles content generation, file uploads, and manages concurrency using semaphores.

## Initialization

Initialize the service with a `GeminiConfig` object:

```python
from pyflow_ai_stack.services.configs import GeminiConfig
from pyflow_ai_stack.services.gemini_service import GeminiService

config = GeminiConfig(
    api_key="your_google_api_key",
    model_name="gemini-2.0-flash",
    concurrency_limit=5
)
gemini_service = GeminiService(config)
```

## Methods

### `generate_content`

Generates a text response from the Gemini model based on the provided prompt and optional system instructions.

- **`prompt`** (`str`): The main prompt text for the model.
- **`system_instruction`** (`str`, optional): Instructions for the system role (e.g., "Act as a professional translator").
- **`generation_config`** (`dict`, optional): Gemini generation configuration (e.g., `temperature`, `top_p`, etc.).
- **`parts`** (`list`, optional): Additional content parts (e.g., images, audio, or previously uploaded file references).

**Returns**: `str` (the generated text).

### `upload_file`

Uploads a file to Gemini for use in subsequent content generation requests.

- **`temp_path`** (`str`): Local path to the temporary file to be uploaded.
- **`filename`** (`str`): Display name for the file in the Gemini system.
- **`mime_type`** (`str`, optional): MIME type of the file.
- **`remove_after_upload`** (`bool`, default: `False`): Whether to delete the local file after successful upload.

**Returns**: `Any` (The uploaded Gemini file object).

### `ping`

Checks if the Gemini service is healthy and responsive by attempting to retrieve model metadata (which does not consume tokens).

**Returns**: `bool` (`True` if healthy, `False` otherwise).

## Concurrency Management

`GeminiService` uses an `asyncio.Semaphore` based on the `concurrency_limit` specified in the configuration. This ensures that you don't overwhelm the API or exceed rate limits when processing multiple requests concurrently.

## Example: Generating Content with a System Prompt

```python
response = await gemini_service.generate_content(
    prompt="Explain quantum entanglement to a 5-year-old.",
    system_instruction="You are a friendly and simplified science educator."
)
print(response)
```
