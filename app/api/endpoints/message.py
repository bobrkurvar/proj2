from fastapi import APIRouter, status, Depends
from db import get_db_manager, Crud
from typing import Annotated
from db.models import Messages
from sqlalchemy.exc import IntegrityError
from app.exceptions.custom_errors import CustomDbException
import logging

router = APIRouter(tags=['Message'])

log = logging.getLogger(__name__)

DbManagerDep = Annotated[Crud, Depends(get_db_manager)]

@router.delete('', summary='удаление всех сообщений',status_code=status.HTTP_200_OK)
async def delete_all_messages(manager: DbManagerDep):
    log.debug('запрос на удаление всех сообщений')
    await manager.delete(Messages)
