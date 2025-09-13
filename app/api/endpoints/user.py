from fastapi import APIRouter, status, HTTPException

from app.api.schemas.user import UserInput, UserOutput
from app.exceptions.schemas import ErrorResponse
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
    user = await manager.create(User, **user.model_dump())
    log.info('пользователь: %s создан', user.id)
    return user

@router.get('',
            summary='список пользователей',
            status_code=status.HTTP_200_OK,
            response_model=List[UserOutput],
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'detail': 'Список пользователей пуст',
                    'model': ErrorResponse
                }
            }
)
async def read_user(ident: str | None = None, ident_val: int | str | None = None):
    if not ident:
        log.debug('запрос на чтение всех пользователей')
        user = await manager.read(User)
    else:
        log.debug('запрос на чтение пользователя %s', ident_val)
        user = await manager.read(model=User, ident=ident, ident_val=ident_val)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Список пользователей пуст'
        )

    return user


@router.delete('{user_id}',
            summary='чтение пользователя',
            status_code=status.HTTP_200_OK,
            response_model=UserOutput
            )
async def delete_from_bot(user_id:int):
    log.debug('запрос на удаление пользователя: %s', user_id)
    user = await manager.delete(User, user_id)
    log.info('пользователь: %s удалён', user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь для удаления не найден'
        )
    return user





