import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dto import UserDelete, UserInput

from app.domain import User, Task
from app.adapters.crud import Crud, get_db_manager

router = APIRouter(tags=["Users"], prefix="users")
log = logging.getLogger(__name__)
dbManagerDep = Annotated[Crud, Depends(get_db_manager)]


@router.get("/{owner_id}/own-tasks")
async def read_users_own_tasks(owner_id: int, manager: dbManagerDep):
    return await manager.read(Task, owner_id=owner_id)


@router.get("/{user_id}/tasks")
async def read_users_tasks(user_id: int, manager: dbManagerDep):
    return await manager.read(Task, to_join=["task_executors"], user_id=user_id)


@router.post("")
async def crete_user(user: UserInput, manager: dbManagerDep):
    log.debug("запрос на создание пользователя: %s", user.id)
    user = await manager.create(User, **user.model_dump())
    log.debug("пользователь: %s создан", user.get("id"))
    return user


@router.get("")
async def read_user_by_criteria(
    manager: dbManagerDep, username: str | None = None, activity: bool | None = None
):
    filters = locals()
    filters.pop("manager")
    return await manager.read(User, **filters)


@router.delete("/{user_id}")
async def delete_by_id(user_id: int, manager: dbManagerDep):
    log.debug("запрос на удаление пользователя: %s", user_id)
    return await manager.delete(User, ident_val=user_id)


@router.delete("")
async def delete_by_criteria(user: UserDelete, manager: dbManagerDep):
    filters = user.model_dump()
    await manager.delete(User, **filters)
