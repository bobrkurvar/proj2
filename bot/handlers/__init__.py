from aiogram import Router
from . import command_core, todo, todo_with_state

main_router = Router()
main_router.include_router(command_core.router)
main_router.include_router(todo.router)
main_router.include_router(todo_with_state.router)