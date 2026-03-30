import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Body

from app.api.dto import TaskInput
from app.domain import Task
from app.adapters.crud import Crud, get_db_manager
from app.services.tasks import make_request, response_to_request, create_task, read_task

router = APIRouter(tags=["Todo"], prefix="tasks")
log = logging.getLogger(__name__)
dbManagerDep = Annotated[Crud, Depends(get_db_manager)]


@router.get("/{task_id}")
async def read_task_by_id(user_id: int, task_id: int, manager: dbManagerDep):
    log.debug("ЗАПРОС НА ЧТЕНИЕ ЗАДАЧИ ПО ID %s", task_id)
    res = await read_task(manager=manager, user_id=user_id, task_id=task_id)
    return res


@router.post("")
async def create_task(task: TaskInput, manager: dbManagerDep):
    task = task.model_dump()
    log.debug("запрос на создание задания")
    todo = await create_task(manager=manager, **task)
    log.debug(f"задача {todo} создана")
    return todo


@router.post("/{task_id}/request")
async def create_request_to_task(
    task_id: int,
    user_id: Annotated[int, Body],
    owner_id: Annotated[int, Body],
    manager: dbManagerDep,
):
    if owner_id == "":
        owner_id = None
    await make_request(
        task_id=task_id, user_id=user_id, owner_id=owner_id, manager=manager
    )


@router.delete("/{task_id}/request")
async def accept_request(
    task_id: int,
    user_id: Annotated[int, Body],
    manager: dbManagerDep,
    accept: bool
):
    await response_to_request(
        manager=manager,
        accept=accept,
        task_id=task_id,
        user_id=user_id,
    )



@router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, manager: dbManagerDep):
    todo = await manager.delete(domain_model=Task, task_id=task_id)
    return todo


