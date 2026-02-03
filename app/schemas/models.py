"""
Pydantic schemas for the application.

This module defines the data models used for API requests and responses.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class GlobalFile(BaseModel):
    """
    Schema for a file shared across multiple tasks.

    Attributes:
        uri (str): URI of the file (e.g., S3 URL).
        mime_type (str): MIME type of the file.
    """

    uri: str
    mime_type: str


class TaskRequest(BaseModel):
    """
    Schema for an individual task request.

    Attributes:
        task_id (str): Unique identifier for the task.
        prompt (str): Prompt to be processed by Gemini.
    """

    task_id: str
    prompt: str


class BatchRequest(BaseModel):
    """
    Schema for a batch of task requests.

    Attributes:
        project_id (str): Unique identifier for the project.
        mode (str): Execution mode, defaults to "sync".
        global_files (List[GlobalFile], optional): Files shared across all tasks.
        tasks (List[TaskRequest]): List of individual tasks to process.
        webhook_url (str, optional): URL to notify upon completion (for async mode).
    """

    project_id: str
    mode: Literal["sync", "async"] = "sync"
    global_files: Optional[List[GlobalFile]] = None
    tasks: List[TaskRequest]
    webhook_url: Optional[str] = None


class TaskResponse(BaseModel):
    """
    Schema for an individual task response.

    Attributes:
        task_id (str): Unique identifier for the task.
        status (str): Status of the task (e.g., "success", "error").
        result (str, optional): Result content from Gemini.
        error (str, optional): Error message if the task failed.
    """

    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None


class BatchResponse(BaseModel):
    """
    Schema for a batch response.

    Attributes:
        project_id (str): Unique identifier for the project.
        results (List[TaskResponse]): List of results for each task in the batch.
    """

    project_id: str
    results: List[TaskResponse]


class HealthResponse(BaseModel):
    """
    Schema for the health check response.

    Attributes:
        status (str): Overall health status ("healthy" or "unhealthy").
        app (str): Name of the application.
        redis (str, optional): Connection status for Redis.
        gemini (str, optional): Connection status for Gemini.
        s3 (str, optional): Connection status for S3.
    """

    status: str
    app: str
    redis: Optional[str] = None
    gemini: Optional[str] = None
    s3: Optional[str] = None
