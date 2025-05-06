
from fastapi import FastAPI
from app.api.endpoints import user_router, todo_router
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import request_validation_exception_handler, global_exception_handler, custom_exception_handler
from app.exceptions.custom_errors import CustomException
from contextlib import asynccontextmanager
from bot.utils import init_external_api_session, close_external_api_manager
from db import manager

@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_external_api_session()
    yield
    await close_external_api_manager()
    await manager.close_and_dispose()

app = FastAPI(lifespan = lifespan)

app.include_router(user_router, prefix='/user')
app.include_router(todo_router, prefix='/todo')

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)