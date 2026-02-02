import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.core.logger import logger
from app.schemas.models import BatchRequest, BatchResponse, TaskResponse
from app.services.gemini_service import gemini_service

router = APIRouter()


async def process_task(task, global_parts):
    try:
        result = await gemini_service.generate_content(
            task.prompt, parts=list(global_parts)
        )
        return TaskResponse(task_id=task.task_id, status="success", result=result)
    except Exception as e:
        logger.error(f"Error processing task {task.task_id}: {str(e)}")
        return TaskResponse(task_id=task.task_id, status="failed", error=str(e))


async def run_async_batch(request: BatchRequest):
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
