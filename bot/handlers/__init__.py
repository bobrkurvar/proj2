from aiogram import Router
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from bot.utils.middleware import DeleteUsersMessage
from . import command_core, paginate_todo, todo_with_state

main_router = Router()
main_router.include_routers(command_core.router, paginate_todo.router, todo_with_state.router)

main_router.callback_query.outer_middleware(CallbackAnswerMiddleware())
main_router.message.outer_middleware(DeleteUsersMessage())
