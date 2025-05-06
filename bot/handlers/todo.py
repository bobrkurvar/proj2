from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from bot.keyboards.todo_keyboard import get_inline_kb
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.utils import get_external_api_session_manager
from bot.lexicon import list_todo_view, start, empty_todo_list, edit_task

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})), StateFilter(default_state))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo):
    indent_attr = "doer_id"
    indent_val = callback.from_user.id
    offsets = {'list': lambda x: x,
               '<<': lambda x: x-callback_data.limit if x > 0 else x,
               '>>': lambda x: x+callback_data.limit}
    offset = offsets[callback_data.act](callback_data.offset)
    manager = await get_external_api_session_manager('todo')
    todo_id = callback_data.offset
    res = list(await manager.read(indent_attr = indent_attr, indent_val = indent_val, offset=offset, limit=3))
    if res:
        res_text = ''
        todo_id = res[0]['id']
        for i in res:
            res_text += list_todo_view.format(i['name'], i['content'])
    else:
        offset = callback_data.offset
        if callback.message.text == start:
            res_text = empty_todo_list
        else:
            res_text = callback.message.text

    params = {'doer_id': callback.from_user.id, 'id':todo_id, 'offset': offset,  'act': callback_data.act}
    buttons_acts = ('<<', 'EDIT', '>>')
    kb = get_inline_kb(width=3, *buttons_acts, **params)
    await callback.message.answer(text = res_text, reply_markup=kb)
    await callback.answer()
    await callback.message.delete()

@router.message(Command(commands=['list']), StateFilter(default_state))
async def process_user_todo_list_command(message: Message):
    indent_attr = "doer_id"
    indent_val = message.from_user.id
    manager = await get_external_api_session_manager('todo')
    res = list(await manager.read(indent_attr=indent_attr, indent_val=indent_val, offset=0, limit=3))
    if res:
        res_text = ''
        for i in res:
            res_text += list_todo_view.format(i['name'], i['content'])
    else:
        if message.text == start:
            res_text = empty_todo_list
        else:
            res_text = message.text

    params = {'doer_id': message.from_user.id, 'id': res[0]['id'], 'offset': 0, 'act': 'list'}
    buttons_acts = ('<<<', 'EDIT', '>>')
    kb = get_inline_kb(width=3, *buttons_acts, **params)
    await message.answer(text = res_text, reply_markup=kb)
    await message.delete()

@router.callback_query(CallbackFactoryTodo.filter(F.data == 'EDIT'), StateFilter(default_state))
async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo):
    await callback.answer()
    params = {'doer_id': callback.from_user.id, 'id': callback_data.id, 'offset': callback_data.offset}
    buttons_acts =  ('EDIT NAME', 'EDIT CONTENT', 'EDIT DATE')
    kb = get_inline_kb(*buttons_acts, **params)
    await callback.message.answer(text=edit_task, reply_markup=kb)
    await callback.message.delete()


