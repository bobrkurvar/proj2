from aiogram import Router
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from bot.utils.middleware import DeleteUsersMessage
from . import command_core, todo, todo_with_state

main_router = Router()
main_router.include_routers(command_core.router, todo.router, todo_with_state.router)

main_router.callback_query.middleware(CallbackAnswerMiddleware())
main_router.message.middleware(DeleteUsersMessage())
