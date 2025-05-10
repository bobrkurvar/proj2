from fastapi import APIRouter
from db import manager
from db.models import Todo
from app.api.schemas.todo import TodoInput

router = APIRouter()

@router.get('/read')
async def read_todo_list(indent_attr: str, indent_val: int):
    res = await manager.read(Todo, indent = (indent_attr, indent_val))
    return res

@router.post('/create')
async def create_task(todo: TodoInput):
    await manager.create(Todo, **todo.model_dump())

@router.delete('/delete')
async def delete_task(todo_id: int):
    await manager.delete(Todo, ident = {'id': todo_id})
