from aiogram import Router

from . import command_core, todo, todo_with_state
import logging

main_router = Router()
main_router.include_routers(command_core.router)
main_router.include_routers(todo.router)
main_router.include_routers(todo_with_state.router)
