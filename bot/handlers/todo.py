from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from bot.utils import MyExternalApiForBot

from bot.keyboards.todo_keyboard import get_inline_kb
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.lexicon import list_todo_view, start, empty_todo_list, edit_task
from bot.states.todo_states import FSMTodoEdit

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})),
                       (StateFilter(default_state, FSMTodoEdit.edit)))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                        ext_api_manager: MyExternalApiForBot, list_id: list, state: FSMContext):
    indent_attr = "doer_id"
    indent_val = callback.from_user.id
    offsets = {'list': lambda x: x,
               '<<': lambda x: x-callback_data.limit if x > 0 else x,
               '>>': lambda x: x+callback_data.limit}
    offset = offsets[callback_data.act](callback_data.offset)
    todo_id = callback_data.offset
    res = list(await ext_api_manager.read(prefix = 'todo', indent_attr = indent_attr, indent_val = indent_val, offset=offset, limit=3))
    if res:
        res_text = ''
        todo_id = res[0]['id']
        res_cnt = 1
        for i in res:
            list_id.append(res[res_cnt-1]['id'])
            res_text += list_todo_view.format(i['name'], i['content']) + edit_task.format(res_cnt)
            res_cnt += 1
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
    await state.set_state(FSMTodoEdit.edit)

@router.message(Command(commands=['list']) , StateFilter(default_state, FSMTodoEdit.edit))
async def process_user_todo_list_command(message: Message, ext_api_manager: MyExternalApiForBot):
    indent_attr = "doer_id"
    indent_val = message.from_user.id
    res = list(await ext_api_manager.read(prefix = 'todo', indent_attr=indent_attr, indent_val=indent_val, offset=0, limit=3))
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





