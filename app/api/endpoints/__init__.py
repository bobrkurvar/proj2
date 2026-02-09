from fastapi import APIRouter

from . import task, user

main_router = APIRouter()
main_router.include_router(todo.router, prefix="/todo")
main_router.include_router(user.router, prefix="/user")
