from fastapi import APIRouter
from db import manager
from db.models import Todo
from app.api.schemas.todo import TodoInput, TodoUpdate
from datetime import date
from typing import Any
from core import logger

router = APIRouter()

@router.get('/read')
async def read_todo_list(ident: str, ident_val: int, limit: int, offset: int = 0):
    res = await manager.read(Todo, ident=ident, ident_val=ident_val, limit=limit, offset=offset)
    return res

@router.post('/create')
async def create_task(todo: TodoInput):
    todo: dict[str, Any] = todo.model_dump()
    todo.update(deadline=date(**todo['deadline']))
    todo_id = await manager.create(Todo, **todo)
    logger.debug(f"задание добавлено: {todo}")
    return todo_id

@router.patch('/update')
async def update_task(todo: TodoUpdate):
    todo_data = todo.model_dump()
    del todo_data['is_delete']
    if not todo_data['name']:
        del todo_data['name']
    if not todo_data['content']:
        del todo_data['content']
    if not todo_data['deadline']:
        del todo_data['deadline']
    else:
        todo_data.update(deadline=date(day=todo_data['deadline']['day'], month=todo_data['deadline']['month'], year=todo_data['deadline']['year']))
    print('-'*100, todo_data, '-'*100, sep='\n')
    await manager.update(Todo, **todo_data)


@router.delete('/delete')
async def delete_task(todo_id: int):
    await manager.delete(Todo, ident = {'id': todo_id})
