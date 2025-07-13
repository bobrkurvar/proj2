from fastapi import APIRouter
from app.api.schemas.user import UserInputFromBot
from db import manager
from db.models import User
import logging

router = APIRouter()
log = logging.getLogger(__name__)

@router.post('/create')
async def crete_user(user: UserInputFromBot):
    log.debug('запрос на создание пользователя: %s', user.id)
    await manager.create(User, **user.model_dump())
    log.info('пользователь: %s создан', user.id)
    return dict(first_name=user.first_name, last_name=user.last_name)

@router.get('/read')
async def read_user(ident: str | None = None, ident_val: int | str | None = None):
    if not ident:
        log.debug('запрос на чтение всех пользователей')
        return await manager.read(User)
    else:
        log.debug('запрос на чтение пользователя %s', ident_val)
        return await manager.read(model=User, ident=ident, ident_val=ident_val)


@router.get('/delete')
async def delete_from_bot(user_id:int):
    log.debug('запрос на удаление пользователя: %s', user_id)
    await manager.delete(User, user_id)
    log.info('пользователь: %s удалён', user_id)
    return {'msg': f"user from {user_id} has been removed"}





