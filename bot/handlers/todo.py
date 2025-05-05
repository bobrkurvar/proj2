from aiogram import Router
from aiogram.types import CallbackQuery
from bot.keyboards.todo_keyboard import get_todo_keyboard
from bot.filters.callback_factory import CallbackFactoryTodo
from db import manager
from db.models import User

router = Router()

@router.callback_query(CallbackFactoryTodo.filter())
async def process_user_todo_list(callback: CallbackQuery):
    ident = {'id': callback.from_user.id}
    res = manager.read(User, **ident)
    await callback.message.answer(text=str(res), reply_markup=get_todo_keyboard())
    await callback.answer()