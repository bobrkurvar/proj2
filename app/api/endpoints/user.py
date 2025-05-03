from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.token import Token
from app.api.schemas.user import UserInputFromBot, UserOutputForBot
from db import manager
from db.models import User
from core.security import create_token
from core import conf
from datetime import timedelta
from typing import Annotated

router = APIRouter()

@router.post('/start-register')
async def register_by_start(user: UserInputFromBot):
    await manager.create(User, **user.model_dump())
    return UserOutputForBot(first_name=user.first_name, last_name=user.last_name)

@router.get('/remove-from-bot')
async def remove_from_bot(user_id:int):
    await manager.delete(User, user_id)
    return {'msg': f"user from {user_id} has been removed"}


# @router.post('/register', dependencies=[Depends(manager.create)])
# async def register(user: UserInput):
#     return UserOutput(username= user.username)
#
# @router.post('/token')
# async def login(result: userFetchFromFromDep):
#     if not result:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     access_token_expire_minutes = conf.ACCESS_TOKEN_EXPIRE_MINUTES
#     data_dict = {'sub': result.first_name}
#     expires_delta = timedelta(minutes=access_token_expire_minutes)
#     token = create_token(data_dict, expires_delta)
#     return Token(access_token=token, token_type="bearer")





