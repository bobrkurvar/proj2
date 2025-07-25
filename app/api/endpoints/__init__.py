from . import todo, user, message
from fastapi import APIRouter

main_router = APIRouter()
main_router.include_router(todo.router, prefix='/todo')
main_router.include_router(user.router, prefix='/user')
main_router.include_router(message.router, prefix='/message')