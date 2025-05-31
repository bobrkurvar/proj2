from fastapi import FastAPI
from app.api.endpoints import main_router
from app.exceptions.handlers import custom_exception_handler, global_exception_handler
from app.exceptions.custom_errors import CustomDbException
from contextlib import asynccontextmanager
from db import manager

@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    manager.close_and_dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomDbException, custom_exception_handler)