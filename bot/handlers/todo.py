from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from bot.keyboards.todo_keyboard import get_inline_kb_current_task
from bot.filters.callback_factory import CallbackFactoryTodo

from db import manager
from db.models import Todo

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo):
    user_ident = ("doer_id", callback.from_user.id)
    offsets = {'<<': lambda x: x-1 if x > 0 else x,
               '>>':  lambda x: x+1,
               'list': lambda x: x}
    offset = offsets[callback_data.act](callback_data.offset)
    res = await manager.read(Todo, user_ident, offset=callback_data.offset, limit=3)
    try:
        res_txt = f"{res[0].get('name')}\n\n{res[0].get('content')}"
        todo_id = res[0].get("id")
    except IndexError:
        res_txt = callback.message.text
        todo_id = callback_data.offset
        offset -= 1 if callback_data.act == '>>' else 0
    params = {'doer_id': callback.from_user.id, 'id': todo_id, 'offset': offset}
    kb = get_inline_kb_current_task('list', **params)
    await callback.message.answer(text =res_txt, reply_markup=kb)
    await callback.message.delete()
    await callback.answer()

@router.message(Command(commands=['list']))
async def process_user_todo_list_command(message: Message):
    user_ident = ("doer_id", message.from_user.id)
    res = await manager.read(Todo, user_ident, limit=1)
    params = {'doer_id': message.from_user.id, 'id': res[0].get("id")}
    kb = get_inline_kb_current_task('list', **params)
    await message.answer(text = f"{res[0].get('name')}\n\n{res[0].get('content')}", reply_markup=kb)
    await message.delete()

# @router.callback_query(CallbackFactoryTodo.filter(F.act == '<<'))
# async def process_swipe_list_left(callback: CallbackQuery, callback_data: CallbackFactoryTodo):
#     user_ident = ("doer_id", callback.from_user.id)
#     swipe_offset = callback_data.offset - 1 if callback_data.offset > 0 else callback_data.offset
#     res = await manager.read(Todo, user_ident, offset=swipe_offset, limit=1)
#     try:
#         res_txt = f"{res[0].get('name')}\n\n{res[0].get('content')}"
#         todo_id = res[0].get("id")
#     except IndexError:
#         res_txt = callback.message.text
#         todo_id = callback_data.offset
#     params = {'doer_id': callback.from_user.id, 'id': todo_id, 'offset': swipe_offset}
#     kb = get_inline_kb_current_task('list', **params)
#     await callback.message.answer(text = res_txt, reply_markup=kb)
#     await callback.answer()
#
# @router.callback_query(CallbackFactoryTodo.filter(F.act == '>>'))
# async def process_swipe_list_left(callback: CallbackQuery, callback_data: CallbackFactoryTodo):
#     user_ident = ("doer_id", callback.from_user.id)
#     swipe_offset = callback_data.offset + 1
#     res = await manager.read(Todo, user_ident, offset=swipe_offset, limit=1)
#     try:
#         res_txt = f"{res[0].get('name')}\n\n{res[0].get('content')}"
#         todo_id = res[0].get("id")
#     except IndexError:
#         swipe_offset -= 1
#         res_txt = callback.message.text
#         todo_id = callback_data.offset
#     params = {'doer_id': callback.from_user.id, 'id': todo_id, 'offset': swipe_offset}
#     kb = get_inline_kb_current_task('list', **params)
#     await callback.message.answer(text=res_txt, reply_markup=kb)
#     await callback.answer()