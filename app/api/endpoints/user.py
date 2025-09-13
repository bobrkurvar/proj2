from fastapi import APIRouter, status

from app.api.schemas.todo import TodoOutput
from app.api.schemas.user import UserInput, UserOutput
from db import manager
from db.models import User
from typing import List
import logging

router = APIRouter(tags=['Users'])
log = logging.getLogger(__name__)

@router.post('',
             summary='создание пользователя',
             status_code=status.HTTP_201_CREATED,
             response_model=UserOutput
)
async def crete_user(user: UserInput):
    log.debug('запрос на создание пользователя: %s', user.id)
    await manager.create(User, **user.model_dump())
    log.info('пользователь: %s создан', user.id)
    return dict(first_name=user.first_name, last_name=user.last_name)

@router.get('',
            summary='список пользователей',
            status_code=status.HTTP_200_OK,
            response_model=List[TodoOutput]
)
async def read_user(ident: str | None = None, ident_val: int | str | None = None):
    if not ident:
        log.debug('запрос на чтение всех пользователей')
        return await manager.read(User)
    else:
        log.debug('запрос на чтение пользователя %s', ident_val)
        return await manager.read(model=User, ident=ident, ident_val=ident_val)


@router.delete('{user_id}',
            summary='чтение пользователя',
            status_code=status.HTTP_200_OK,
            response_model=TodoOutput
            )
async def delete_from_bot(user_id:int):
    log.debug('запрос на удаление пользователя: %s', user_id)
    await manager.delete(User, user_id)
    log.info('пользователь: %s удалён', user_id)





