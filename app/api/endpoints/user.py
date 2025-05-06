from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.user import UserInputFromBot
from db import manager
from db.models import User

router = APIRouter()

@router.post('/create')
async def register_by_start(user: UserInputFromBot):
    await manager.create(User, **user.model_dump())
    return dict(first_name=user.first_name, last_name=user.last_name)

@router.get('/delete')
async def remove_from_bot(user_id:int):
    await manager.delete(User, user_id)
    return {'msg': f"user from {user_id} has been removed"}





