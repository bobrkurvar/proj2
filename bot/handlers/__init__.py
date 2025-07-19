from aiogram import Router
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from bot.utils.middleware import DeleteUsersMessage
from . import command_core, paginate_todo, todo

main_router = Router()
main_router.include_routers(command_core.router, todo.router, paginate_todo.router)

main_router.callback_query.outer_middleware(CallbackAnswerMiddleware())
main_router.message.outer_middleware(DeleteUsersMessage())
