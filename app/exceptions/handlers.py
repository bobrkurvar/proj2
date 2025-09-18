from fastapi.responses import JSONResponse
from fastapi import Request, status
from db.exceptions import NotFoundError, AlreadyExistsError, DatabaseError
import logging

log = logging.getLogger(__name__)

def not_found_in_db_exceptions_handler(request: Request, exc: NotFoundError):
    log.exception('Ошибка поиска в базе данных')
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {
            'code': status.HTTP_404_NOT_FOUND,
            'detail': str(exc)
        }
    )

def entity_already_exists_in_db_exceptions_handler(request: Request, exc: AlreadyExistsError):
    log.exception('Ошибка создания в базе данных')
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content = {
            'code': status.HTTP_409_CONFLICT,
            'description': str(exc)
        }
    )

def data_base_exception_handler(request: Request, exc: DatabaseError):
    log.exception('Ошибка базы данных')
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'description': str(exc)
        }
    )

def global_exception_handler(request: Request, exc):
    log.exception("Глобальная ошибка")
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'description': str(exc)
        }
    )