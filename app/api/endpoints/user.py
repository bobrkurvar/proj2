from fastapi import APIRouter, status, Depends
from app.api.schemas.user import UserInputFromBot
from app.exceptions.custom_errors import CustomDbException
from db import get_db_manager, Crud
from typing import Annotated
from db.models import User
from sqlalchemy.exc import IntegrityError
import logging

router = APIRouter(tags=['Users'])
log = logging.getLogger(__name__)

DbManagerDep = Annotated[Crud, Depends(get_db_manager)]

@router.post('', summary='создание пользователя', status_code=status.HTTP_201_CREATED)
async def crete_user(user: UserInputFromBot, manager: DbManagerDep):
    log.debug('запрос на создание пользователя: %s', user.id)
    try:
        await manager.create(User, **user.model_dump())
    except IntegrityError:
        raise CustomDbException(message='ошибка целостности бд', detail='пользователь с данным id уже существует', status_code=status.HTTP_200_OK)
    return dict(first_name=user.first_name, last_name=user.last_name)

@router.get('/{ident}', summary='список пользователей',status_code=status.HTTP_200_OK)
async def read_user(ident: int, manager: DbManagerDep):
    log.debug('запрос на чтение пользователя %s', ident)
    res = await manager.read(model=User, ident='id', ident_val=ident)
    if res is None:
        raise CustomDbException(message='пользователь не найден', detail='пользователь не найден', status_code=status.HTTP_404_NOT_FOUND)
    return res

@router.get('', summary='список пользователей',status_code=status.HTTP_200_OK)
async def read_user(manager: DbManagerDep):
    log.debug('запрос на чтение всех пользователей')
    res = await manager.read(User)
    if res is None:
        raise CustomDbException(message='пользователь не найден', detail='пользователь не найден', status_code=status.HTTP_404_NOT_FOUND)
    return res

@router.delete('/{ident}', summary='удаление пользователя',status_code=status.HTTP_200_OK)
async def delete_from_bot(ident:int, manager: DbManagerDep):
    log.debug('запрос на удаление пользователя: %s', ident)
    await manager.delete(User, ident)
    return {'msg': f"пользователь {ident} удалён"}





