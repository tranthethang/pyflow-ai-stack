from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.schemas.models import BatchRequest, BatchResponse, TaskResponse
from app.services.gemini_service import gemini_service

router = APIRouter()


@router.post("/run", response_model=BatchResponse)
async def run_batch(request: BatchRequest):
    logger.info(f"Processing batch for project: {request.project_id}")
    results = []

    for task in request.tasks:
        try:
            result = await gemini_service.generate_content(task.prompt)
            results.append(
                TaskResponse(task_id=task.task_id, status="success", result=result)
            )
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {str(e)}")
            results.append(
                TaskResponse(task_id=task.task_id, status="failed", error=str(e))
            )

    return BatchResponse(project_id=request.project_id, results=results)
