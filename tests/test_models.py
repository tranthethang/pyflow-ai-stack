from pyflow_ai_stack.schemas.models import (BatchRequest, BatchResponse,
                                            GlobalFile, HealthResponse,
                                            TaskRequest, TaskResponse)


def test_global_file_schema():
    file = GlobalFile(uri="s3://bucket/file", mime_type="text/plain")
    assert file.uri == "s3://bucket/file"
    assert file.mime_type == "text/plain"


def test_task_request_schema():
    req = TaskRequest(task_id="1", prompt="hello")
    assert req.task_id == "1"
    assert req.prompt == "hello"


def test_batch_request_schema():
    task = TaskRequest(task_id="1", prompt="hello")
    global_file = GlobalFile(uri="s3://uri", mime_type="image/png")
    batch = BatchRequest(
        project_id="proj1",
        mode="async",
        global_files=[global_file],
        tasks=[task],
        webhook_url="http://webhook",
    )
    assert batch.project_id == "proj1"
    assert batch.mode == "async"
    assert len(batch.tasks) == 1
    assert batch.webhook_url == "http://webhook"


def test_task_response_schema():
    resp = TaskResponse(task_id="1", status="success", result="done")
    assert resp.task_id == "1"
    assert resp.status == "success"
    assert resp.result == "done"


def test_batch_response_schema():
    task_resp = TaskResponse(task_id="1", status="success")
    batch_resp = BatchResponse(project_id="proj1", results=[task_resp])
    assert batch_resp.project_id == "proj1"
    assert len(batch_resp.results) == 1


def test_health_response_schema():
    hr = HealthResponse(status="healthy", app="test", redis="connected")
    assert hr.status == "healthy"
    assert hr.redis == "connected"
