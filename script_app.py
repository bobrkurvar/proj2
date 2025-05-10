
from fastapi import FastAPI
from app.api.endpoints import user_router, todo_router
from app.exceptions.handlers import custom_exception_handler, global_exception_handler
from app.exceptions.custom_errors import CustomException


app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(todo_router, prefix='/todo')

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)