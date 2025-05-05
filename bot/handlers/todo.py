from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from bot.keyboards.todo_keyboard import get_inline_kb_current_task
from bot.filters.callback_factory import CallbackFactoryTodo
from db import manager
from db.models import Todo

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act == 'list'))
async def process_user_todo_list_button(callback: CallbackQuery):
    user_ident = ("doer_id", callback.from_user.id)
    res = await manager.read(Todo, user_ident, limit=1)
    params = {'doer_id': callback.from_user.id, 'id': res[0].get("id")}
    kb = get_inline_kb_current_task(**params)
    await callback.message.answer(text = res[0].get('content'), reply_markup=kb)
    await callback.answer()

@router.message(Command(commands=['list']))
async def process_user_todo_list_command(message: Message):
    user_ident = ("doer_id", message.from_user.id)
    res = await manager.read(Todo, user_ident, limit=1)
    params = {'doer_id': message.from_user.id, 'id': res[0].get("id")}
    kb = get_inline_kb_current_task(**params)
    await message.answer(text = res[0].get('content'), reply_markup=kb)