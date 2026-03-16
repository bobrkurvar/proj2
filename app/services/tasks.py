from .UoW import UnitOfWork
from app.domain import RequestsToExecutor, TaskExecutors, Task, AlreadyExistsError
from datetime import datetime


async def make_request(
    manager,
    user_id: int,
    task_id: int,
    owner_request: bool,
):
    try:
        return await manager.create(
            RequestsToExecutor,
            task_id=task_id,
            user_id=user_id,
            owner_request=owner_request,
        )
    except AlreadyExistsError:
        return await response_to_request(manager, user_id, task_id, owner_request)


async def response_to_request(
    manager,
    user_id: int,
    task_id: int,
    owner_request: bool,
    accept: bool = True,
    uow_class=UnitOfWork,
):
    async with uow_class(manager) as uow:
        await manager.delete(
            RequestsToExecutor,
            task_id=task_id,
            user_id=user_id,
            owner_request=owner_request,
            session=uow.session,
        )
        if accept:
            return await manager.create(
                TaskExecutors, task_id=task_id, user_id=user_id, session=uow.session
            )


async def create_task(
    manager,
    owner_id: int,
    description: str,
    deadline: datetime,
    public: bool,
    executors: list,
    uow_class=UnitOfWork,
):
    async with uow_class(manager) as uow:
        task = await manager.create(
            Task,
            owner_id=owner_id,
            description=description,
            deadline=deadline,
            public=public,
            session=uow.session,
        )
        await manager(TaskExecutors, user_id=owner_id, task_id=task["id"])
        requests_to_executors = [
            {"user_id": executor, "task_id": task["id"], "owner_request": True}
            for executor in executors
        ]
        await manager.create(RequestsToExecutor, seq_data=requests_to_executors)
        return task
