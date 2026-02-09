from .UoW import UnitOfWork
from app.domain import RequestsToExecutor, TaskExecutors, Task
from datetime import datetime

async def make_request(
        manager,
        user_id: int,
        task_id: int,
        owner_request: bool,
        uow_class=UnitOfWork
):
    async with uow_class(manager._session_factory) as uow:
        exists_counter_request = await manager.read(RequestsToExecutor, task_id=task_id, user_id=user_id, owner_request = not owner_request, session=uow.session)
        if not exists_counter_request:
            return await manager.create(RequestsToExecutor, task_id=task_id, user_id=user_id, owner_request = owner_request, session=uow.session)
        else:
            return accept_request(manager, user_id, task_id, owner_request, session=uow.session)


async def accept_request(
    manager,
    user_id: int,
    task_id: int,
    owner_request: bool,
    session = None,
    uow_class=UnitOfWork
):
    async def _accept_internal(session):
        await manager.delete(RequestsToExecutor, task_id=task_id, user_id=user_id, owner_request=owner_request, session=session)
        return await manager.create(TaskExecutors, task_id=task_id, user_id=user_id, session=session)

    if session:
        return await _accept_internal(session)
    async with uow_class(manager._session_factory) as uow:
        return await _accept_internal(uow.session)


async def create_task(
    manager,
    owner_id: int,
    description: str,
    deadline: datetime,
    public: bool,
    executors: list,
    uow_class=UnitOfWork
):
    async with uow_class(manager._session_factory) as uow:
        task = await manager.create(Task, owner_id=owner_id, description=description, deadline=deadline, public=public, session=uow.session)
        requests_to_executors = [{"user_id": executor, "task_id": task["id"], "owner_request": True} for executor in executors]
        await manager.create(RequestsToExecutor, seq_data=requests_to_executors)
        return task