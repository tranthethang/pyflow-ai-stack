from typing import List, Optional

from pydantic import BaseModel, Field


class GlobalFile(BaseModel):
    uri: str
    mime_type: str


class TaskRequest(BaseModel):
    task_id: str
    prompt: str


class BatchRequest(BaseModel):
    project_id: str
    mode: str = "sync"
    global_files: Optional[List[GlobalFile]] = None
    tasks: List[TaskRequest]
    webhook_url: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None


class BatchResponse(BaseModel):
    project_id: str
    results: List[TaskResponse]
