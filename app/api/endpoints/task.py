import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Body

from app.api.schemas.task import TaskInput, TaskUpdate
from app.domain.task import Task
from app.adapters.crud import Crud, get_db_manager
from app.services.tasks import make_request, accept_request, create_task

router = APIRouter(tags=["Todo"])
log = logging.getLogger(__name__)
dbManagerDep = Annotated[Crud, Depends(get_db_manager)]


@router.get("")
async def read_task_by_criteria(
    manager: dbManagerDep,
    owner_id: int,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
):
    log.debug(
        "запрос на чтение задач по doer_id со значением: %s limit: %s, offset: %s",
        owner_id,
        limit,
        offset,
    )
    res = await manager.read(
        Task,
        owner_id=owner_id,
        limit=limit,
        offset=offset,
        order_by=order_by,
    )
    return res


@router.get("/{task_id}")
async def read_task_by_id(task_id: int, manager: dbManagerDep):
    log.debug("ЗАПРОС НА ЧТЕНИЕ ЗАДАЧИ ПО ID %s", task_id)
    res = await manager.read(Task, task_id=task_id)
    return res


@router.post("")
async def create_task(task: TaskInput, manager: dbManagerDep):
    task = task.model_dump()
    log.debug("запрос на создание задания")
    todo = await create_task(manager=manager, **task)
    log.debug(f"задача {todo} создана")
    return todo


@router.post("/{task_id}/request")
async def create_request_to_task(task_id: int, user_id: Annotated[int, Body], owner_request: Annotated[bool, Body], manager: dbManagerDep):
    await make_request(task_id=task_id, user_id=user_id, owner_request=owner_request, manager=manager)


@router.delete("/{task_id}/request")
async def delete_request(task_id: int, user_id: Annotated[int, Body], owner_request: Annotated[bool, Body], manager: dbManagerDep):
    await accept_request(manager=manager, task_id=task_id, user_id=user_id, owner_request=owner_request)

# @router.patch("")
# async def update_task(task: TaskUpdate, manager: dbManagerDep):
#     todo_data = task.model_dump()
#     for_update = []
#     del todo_data["is_delete"]
#     if not todo_data["name"]:
#         del todo_data["name"]
#     else:
#         for_update.append("name")
#
#     if not todo_data["content"]:
#         del todo_data["content"]
#     else:
#         for_update.append("content")
#
#     if not todo_data["deadline"]:
#         del todo_data["deadline"]
#     else:
#         todo_data.update(
#             deadline=date(
#                 day=todo_data["deadline"]["day"],
#                 month=todo_data["deadline"]["month"],
#                 year=todo_data["deadline"]["year"],
#             )
#         )
#         for_update.append("deadline")
#     log.debug(
#         "Запрос на обновление в задании " "%s параметров: %s",
#         todo.ident_val,
#         *for_update,
#     )
#     await manager.update(Todo, **todo_data)


@router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, manager: dbManagerDep):
    todo = await manager.delete(domain_model=Task, task_id=task_id)
    return todo

