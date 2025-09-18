from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from app.api.schemas.user import UserInput, UserOutput, UserDelete
from app.exceptions.schemas import ErrorResponse
from sqlalchemy.exc import IntegrityError, NoResultFound
from db import manager
from db.models import User
from typing import List, Annotated
import logging

router = APIRouter(tags=['Users'])
log = logging.getLogger(__name__)

@router.post('',
             summary='создание пользователя',
             status_code=status.HTTP_201_CREATED,
             response_model=UserOutput,
             responses={
                 status.HTTP_409_CONFLICT: {
                     'detail': 'Пользователь с таким id уже существует',
                     'model': ErrorResponse
                 }
             }
)
async def crete_user(user: UserInput):
    log.debug('запрос на создание пользователя: %s', user.id)
    # try:
    user = await manager.create(User, **user.model_dump())
    log.info('пользователь: %s создан', user.get('id'))
    # except IntegrityError:
    #     raise HTTPException(
    #         status_code = status.HTTP_409_CONFLICT,
    #         detail = 'Пользователь с таким id уже существует'
    #     )
    return user

@router.get('',
            summary='список пользователей',
            status_code=status.HTTP_200_OK,
            response_model=List[UserOutput],
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'detail': 'Список пользователей пуст или данный пользователь не найден',
                    'model': ErrorResponse
                }
            }
)
async def read_user_by_criteria(username: str | None = None, activity: bool | None = None):
    user = None
    if (username is None) and (activity is None):
        log.debug('запрос на чтение всех пользователей')
        user = await manager.read(User)
    else:
        if not (username is None):
            log.debug('запрос на чтение пользователя с username: %s', username)
            user = await manager.read(model=User, ident='username', ident_val=username)
        elif not (activity is None):
            log.debug('запрос на чтение пользователя с активностью: %s', activity)
            user = await manager.read(model=User, ident='activity', ident_val=activity)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Список пользователей пуст' if (username is None) and (activity is None) else 'Пользователь не найден'
        )
    return user

@router.delete('{user_id}',
            summary='Удаление пользователя по id',
            status_code=status.HTTP_200_OK,
            response_model=UserOutput,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'detail': 'Пользователь не найден',
                    'model': ErrorResponse
                }
            }
)
async def delete_by_id(user_id: int):
    log.debug('запрос на удаление пользователя: %s', user_id)
    user = await manager.delete(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь для удаления не найден'
        )
    return user

@router.delete('',
               summary='Удаление пользователей по критериям',
               responses={
                   status.HTTP_404_NOT_FOUND: {
                       'detail': 'Пользователи не найдены',
                       'model': ErrorResponse
                   },
                   status.HTTP_204_NO_CONTENT: {
                       'detail': 'Пользователи удалены'
                   }
               }
)
async def delete_by_criteria(user: UserDelete):
    try:
        if not (user.username is None):
            log.debug('Запрос на удаление пользователя по критерию %s с значением %s', 'username', user.username)
            await manager.delete(User, ident='username', ident_val=user.username)
        elif not (user.activity is None):
            log.debug('Запрос на удаление пользователя по критерию %s с значением %s', 'activity', user.activity)
            await manager.delete(User, ident='activity', ident_val=user.activity)
        else:
            log.debug('Запрос на удаление всех пользователей')
            await manager.delete(User)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователи не найдены'
        )





