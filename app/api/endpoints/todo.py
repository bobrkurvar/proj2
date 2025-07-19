from fastapi import APIRouter, status, Depends
from db import get_db_manager, Crud
from typing import Annotated
from db.models import Todo
from app.api.schemas.todo import TodoInput, TodoUpdate
from sqlalchemy.exc import IntegrityError
from app.exceptions.custom_errors import CustomDbException
from datetime import date
import logging

router = APIRouter(tags=['Todo'])

log = logging.getLogger(__name__)

DbManagerDep = Annotated[Crud, Depends(get_db_manager)]

@router.get('/{ident}',status_code=status.HTTP_200_OK, summary='получение задачи')
async def read_todo_list(ident: int, manager: DbManagerDep):
    log.debug('запрос на чтение задачи по id со значением: %s limit: %s')
    res = await manager.read(Todo, ident='id', ident_val=ident)
    if res is None:
        raise CustomDbException(message='задача не найдена', detail='задача не найдена', status_code=status.HTTP_404_NOT_FOUND)
    return res

@router.get('',status_code=status.HTTP_200_OK, summary='получение списка задач')
async def read_todo_list(ident: str, ident_val: int,
                         manager: DbManagerDep, limit: int | None = None, offset: int | None = None, order_by: str | None = None):
    log.debug('запрос на чтение задач по %s со значением: %s limit: %s, offset: %s', ident, ident_val, limit, offset)
    res = await manager.read(Todo, ident=ident, ident_val=ident_val, limit=limit, offset=offset, order_by = order_by)
    return res

@router.post('',status_code=status.HTTP_201_CREATED, summary='создание задачи')
async def create_task(todo: TodoInput, manager: DbManagerDep):
    todo = todo.model_dump()
    todo.update(deadline=date(**todo.get('deadline')))
    log.debug('запрос на создание задания')
    try:
        todo_id = await manager.create(Todo, **todo)
    except IntegrityError as err:
        msg_err = str(err.orig)
        if "foreign key constraint" in msg_err:
            raise CustomDbException(message='ошибка целостности бд', detail='пользователя с таким doer_id не существует',
                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise CustomDbException(message='ошибка целостности бд', detail='задача с таким id уже существует',
                                    status_code=status.HTTP_200_OK)
    return todo_id

@router.patch('', summary='обновление данных задачи', status_code=status.HTTP_200_OK)
async def update_task(todo: TodoUpdate, manager: DbManagerDep):
    todo_data = todo.model_dump()
    for_update = []
    del todo_data['is_delete']
    if not todo_data['name']:
        del todo_data['name']
    else:
        for_update.append('name')

    if not todo_data['content']:
        del todo_data['content']
    else:
        for_update.append('content')

    if not todo_data['deadline']:
        del todo_data['deadline']
    else:
        todo_data.update(deadline=date(day=todo_data['deadline']['day'], month=todo_data['deadline']['month'], year=todo_data['deadline']['year']))
        for_update.append('deadline')
    log.debug('запрос на обновление в задании %s параметров: %s', todo.ident_val, *for_update)
    await manager.update(Todo, **todo_data)


@router.delete('/{ident}', summary='удаление задачи', status_code=status.HTTP_200_OK)
async def delete_task(manager: DbManagerDep, ident: int):
    log.debug('запрос на удаление задания %s', ident)
    await manager.delete(Todo, ident = {'id': ident})


@router.delete('', summary='удаление задач', status_code=status.HTTP_200_OK)
async def delete_task(manager: DbManagerDep):
    log.debug('запрос на удаление всех заданий')
    await manager.delete(Todo)
