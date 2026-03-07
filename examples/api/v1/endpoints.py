"""
API endpoints for version 1.

This module defines the routes for processing tasks and batches, including
support for synchronous and asynchronous execution modes.
"""

import httpx
from fastapi import APIRouter, BackgroundTasks

from examples.core.logger import logger
from examples.core.services import get_gemini_service
from pyflow_ai_stack.schemas.models import BatchRequest, BatchResponse, TaskResponse

router = APIRouter()


async def process_task(task, global_parts):
    """
    Process a single task using Gemini.

    Args:
        task (TaskRequest): The task to process.
        global_parts (list): Shared content parts (files) for the task.

    Returns:
        TaskResponse: The result of the task execution.
    """
    try:
        result = await get_gemini_service().generate_content(
            task.prompt, parts=global_parts
        )
        return TaskResponse(task_id=task.task_id, status="success", result=result)
    except Exception as e:
        logger.error(f"Error processing task {task.task_id}: {str(e)}")
        return TaskResponse(task_id=task.task_id, status="failed", error=str(e))


async def run_async_batch(request: BatchRequest):
    """
    Process a batch of tasks asynchronously in the background.

    Args:
        request (BatchRequest): The batch request containing tasks and files.
    """
    global_parts = []
    if request.global_files:
        for f in request.global_files:
            global_parts.append(
                {"file_data": {"mime_type": f.mime_type, "file_uri": f.uri}}
            )

    results = []
    for task in request.tasks:
        res = await process_task(task, global_parts)
        results.append(res)

    batch_response = BatchResponse(project_id=request.project_id, results=results)

    if request.webhook_url:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(request.webhook_url, json=batch_response.model_dump())
                logger.info(f"Webhook sent to {request.webhook_url}")
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")


@router.post("/run", response_model=BatchResponse)
async def run_batch(request: BatchRequest, background_tasks: BackgroundTasks):
    """
    Execute a batch of tasks.

    Depending on the mode, tasks are either processed synchronously or
    added to background tasks for asynchronous processing.

    Args:
        request (BatchRequest): The batch request data.
        background_tasks (BackgroundTasks): FastAPI background tasks handler.

    Returns:
        BatchResponse: Synchronous results or an acknowledgment for async mode.
    """
    logger.info(
        f"Processing batch for project: {request.project_id} | Mode: {request.mode}"
    )

    if request.mode == "async":
        background_tasks.add_task(run_async_batch, request)
        return BatchResponse(project_id=request.project_id, results=[])

    global_parts = []
    if request.global_files:
        for f in request.global_files:
            global_parts.append(
                {"file_data": {"mime_type": f.mime_type, "file_uri": f.uri}}
            )

    results = []
    for task in request.tasks:
        res = await process_task(task, global_parts)
        results.append(res)

    return BatchResponse(project_id=request.project_id, results=results)
