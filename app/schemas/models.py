from typing import List, Optional

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    task_id: str
    prompt: str


class BatchRequest(BaseModel):
    project_id: str
    tasks: List[TaskRequest]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None


class BatchResponse(BaseModel):
    project_id: str
    results: List[TaskResponse]
