import pytest
from app.services.tasks import create_task, make_request, response_to_request
from app.domain import Task, TaskExecutors, RequestsToExecutor
from tests.fakes import FakeUoW
from datetime import datetime


@pytest.mark.asyncio
async def test_request_user_to_owner_create_success(crud):
    owner_id, username, description, deadline = 11, "username", "description", datetime(day=1, month=1, year=2027)
    task = await crud.create(Task, owner_id=owner_id, description=description, deadline=deadline)
    user_id, task_id = 12, task["id"]
    request = await make_request(crud, user_id=user_id, task_id=task_id)
    request_in_db = await crud.read(RequestsToExecutor, user_id=user_id, task_id=task_id)
    assert request and request["task_id"] == task_id and request["user_id"] == user_id and not request["owner_request"]
    assert request_in_db


@pytest.mark.asyncio
async def test_request_from_owner_create_success(crud):
    owner_id, username, description, deadline = 11, "username", "description", datetime(day=1, month=1, year=2027)
    task = await crud.create(Task, owner_id=owner_id, description=description, deadline=deadline)
    user_id, task_id = 12, task["id"]
    request = await make_request(crud, user_id=user_id, task_id=task_id, owner_id=owner_id)
    request_in_db = await crud.read(RequestsToExecutor, user_id=user_id, task_id=task_id)
    assert request and request["task_id"] == task_id and request["user_id"] == user_id and request["owner_request"]
    assert request_in_db


@pytest.mark.asyncio
async def test_response_to_request_accept(crud):
    owner_id, user_id, username, description, deadline = 11, 12, "username", "description", datetime(day=1, month=1, year=2027)
    task = await crud.create(Task, owner_id=owner_id, description=description, deadline=deadline)
    # просто добавляем этот запрос, логике проверки уже в сервисной функции
    await crud.create(RequestsToExecutor, user_id=user_id, task_id=task["id"], owner_id=owner_id)
    await response_to_request(crud, user_id=user_id, task_id=task["id"], uow_class=FakeUoW)
    requests_in_db = await crud.read(RequestsToExecutor)
    executor_in_db = await crud.read(TaskExecutors, user_id=user_id)
    assert not requests_in_db
    assert executor_in_db


@pytest.mark.asyncio
async def test_response_to_request_not_accept(crud):
    owner_id, user_id, username, description, deadline = 11, 12, "username", "description", datetime(day=1, month=1, year=2027)
    task = await crud.create(Task, owner_id=owner_id, description=description, deadline=deadline)
    # просто добавляем этот запрос, логике проверки уже в сервисной функции
    await crud.create(RequestsToExecutor, user_id=user_id, task_id=task["id"], owner_id=owner_id)
    await response_to_request(crud, user_id=user_id, task_id=task["id"], uow_class=FakeUoW, accept=False)
    requests_in_db = await crud.read(RequestsToExecutor)
    executor_in_db = await crud.read(TaskExecutors, user_id=user_id)
    assert not requests_in_db
    assert not executor_in_db


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
    # можно передать id тех, кому нужно послать запрос на совместное выполнение задачи
    executors = [1, 2, 3]
    task = await create_task(crud, owner_id=owner_id, description=description, uow_class=FakeUoW, deadline=deadline, executors=executors)
    task_in_db = await crud.read(Task, owner_id=owner_id)
    task_executors = await crud.read(TaskExecutors)
    task_requests = await crud.read(RequestsToExecutor)
    assert len(task_requests) == 3
    # пока исполнитель, только создатель задачи
    assert len(task_executors) == 1
    assert task and "id" in task
    assert task_in_db and task_executors


