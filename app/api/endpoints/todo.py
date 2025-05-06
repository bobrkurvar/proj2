from fastapi import APIRouter
from db import manager
from db.models import Todo

router = APIRouter()

@router.get('/read')
async def read_todo_list(indent_attr: str, indent_val: int, offset: int, limit: int):
    res = await manager.read(Todo, indent = (indent_attr, indent_val), offset = offset, limit = limit)
    return res