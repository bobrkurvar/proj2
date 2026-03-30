import pytest
from app.services.tasks import create_task
from app.domain import Task, TaskExecutors, RequestsToExecutor
from tests.fakes import FakeUoW
from datetime import datetime

@pytest.mark.asyncio
async def test_task_create_success(crud):
    owner_id, username, description, deadline = 11, "username", "description", datetime(day=1, month=1, year=2027)
    task = await create_task(crud, owner_id=owner_id, description=description, uow_class=FakeUoW, deadline=deadline)
    task_in_db = await crud.read(Task, owner_id=owner_id)
    task_executors = await crud.read(TaskExecutors)
    assert len(task_executors) == 1
    assert task and "id" in task
    assert task_in_db
    assert len(task_executors) == 1 and task_executors[0]["user_id"] == owner_id


@pytest.mark.asyncio
async def test_task_create_success_with_executors(crud):
    owner_id, username, description, deadline = 11, "username", "description", datetime(day=1, month=1, year=2027)
    executors = [1, 2, 3]
    task = await create_task(crud, owner_id=owner_id, description=description, uow_class=FakeUoW, deadline=deadline, executors=executors)
    task_in_db = await crud.read(Task, owner_id=owner_id)
    task_executors = await crud.read(TaskExecutors)
    task_requests = await crud.read(RequestsToExecutor)
    assert len(task_requests) == 3
    assert len(task_executors) == 4
    assert task and "id" in task
    assert task_in_db and task_executors