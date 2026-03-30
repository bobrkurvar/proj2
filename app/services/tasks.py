from .UoW import UnitOfWork
from app.domain import RequestsToExecutor, TaskExecutors, Task, AlreadyExistsError, TaskNotFoundError
from datetime import datetime
import logging

log = logging.getLogger(__name__)


# async def is_owner(user_id: int | None, manager=None, task: dict = None, task_id: int = None):
async def is_owner(user_id: int | None, task: dict):
    # try:
    #     if task is None:
    #         log.debug("task id: %s", task_id)
    #         task = (await manager.read(Task, id=task_id))[0]
    # except IndexError:
    #     log.debug("Tasks with id %s not exists", task_id)
    #     raise TaskNotFoundError(task_id=task_id)
    return user_id is not None and task["owner_id"] == user_id


async def make_request(
    manager,
    user_id: int,
    task_id: int,
    owner_id: int = None
):
    try:
        task = (await manager.read(Task, id=task_id))[0]
        user_id_owner = await is_owner(user_id=owner_id, task=task)
        owner_request = True if user_id_owner else False
        log.debug("is owner: %s", owner_request)
        return await manager.create(
            RequestsToExecutor,
            task_id=task_id,
            user_id=user_id,
            owner_request=owner_request,
        )
    except AlreadyExistsError:
        request = await manager.read(
            RequestsToExecutor,
            task_id=task_id,
            user_id=user_id,
            owner_request=(not owner_request),
        )
        log.debug("request: %s", request)
        if request:
            return await response_to_request(manager, user_id, task_id, owner_request)
    except IndexError:
        log.debug("Tasks with id %s not exists", task_id)
        raise TaskNotFoundError(task_id=task_id)


async def response_to_request(
    manager,
    user_id: int,
    task_id: int,
    #owner_request: bool,
    accept: bool = True,
    uow_class=UnitOfWork,
):
    # if owner_request is None:
    #     user_is_owner = await is_owner(user_id=user_id, task_id=task_id, manager=manager)
    #     owner_request = True if user_is_owner else False

    async with uow_class(manager) as uow:
        await manager.delete(
            RequestsToExecutor,
            task_id=task_id,
            user_id=user_id,
            #owner_request=owner_request,
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
    executors: list = None,
    public: bool = True,
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
        await manager.create(TaskExecutors, user_id=owner_id, task_id=task["id"])
        if executors:
            requests_to_executors = [
                {"user_id": executor, "task_id": task["id"], "owner_request": True}
                for executor in executors
            ]
            log.debug("requests: %s", requests_to_executors)
            await manager.create(RequestsToExecutor, seq_data=requests_to_executors)
        return task


async def read_task(manager, user_id: int, task_id):
    is_executor = await manager.read(TaskExecutors, user_id=user_id, task_id=task_id)
    if is_executor:
        return await (manager.read(Task, task_id=task_id))[0]