from fastapi import APIRouter
from db import manager
from db.models import Todo
from app.api.schemas.todo import TodoInput, TodoUpdate
from datetime import date
from typing import Any
import logging

router = APIRouter()

log = logging.getLogger(__name__)

@router.get('/read')
async def read_todo_list(ident: str, ident_val: int, limit: int | None = None, offset: int | None = None, order_by: str | None = None):
    log.debug('запрос на чтение задач по %s со значением: %s limit: %s, offset: %s', ident, ident_val, limit, offset)
    res = await manager.read(Todo, ident=ident, ident_val=ident_val, limit=limit, offset=offset, order_by = order_by)
    return res

@router.post('/create')
async def create_task(todo: TodoInput):
    todo: dict[str, Any] = todo.model_dump()
    todo.update(deadline=date(**todo['deadline']))
    log.debug('запрос на создание задания')
    todo_id = await manager.create(Todo, **todo)
    log.info("задание %s добавлено", todo_id)
    return todo_id

@router.patch('/update')
async def update_task(todo: TodoUpdate):
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
    log.debug('запрос на обновление в задании '
             '%s параметров: %s', todo.ident_val, *for_update)
    await manager.update(Todo, **todo_data)
    log.info('в задаче: %s обновлены параметры: %s', todo.ident_val, *for_update)


@router.delete('/delete')
async def delete_task(todo_id: int | None = None):
    if todo_id:
        await manager.delete(Todo, ident = {'id': todo_id})
        log.info('задание %s удалено', todo_id)
    else:
        await manager.delete(Todo)
        log.info('все задания пользователя удалены')
