from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from bot.utils import MyExternalApiForBot

from bot.utils.keyboards import get_inline_kb
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.lexicon import list_todo_view, empty_todo_list, edit_task
from bot.states.todo_states import FSMTodoEdit
from core import logger

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})),
                       StateFilter(default_state, FSMTodoEdit.edit))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                        ext_api_manager: MyExternalApiForBot, state: FSMContext):
    indent_attr, indent_val = "doer_id", callback.from_user.id
    limit = callback_data.limit

    offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
               '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}

    offset: int = offsets[callback_data.act]

    if callback_data.act == 'list':
        try:
            res: list[dict] = list(await ext_api_manager.read(prefix = 'todo', indent_attr = indent_attr, indent_val = indent_val))
            logger.info(res)
        except TypeError:
            res = list()
    else:
        res = (await state.get_data()).get('task_list', [])

    if res:
        if len(res) <= offset:
            offset = callback_data.offset
        res_text = ''
        await state.update_data({'task_list': res})
        res_cnt = offset + 1
        for i in range(offset, offset+limit):
            try:
                res_text += list_todo_view.format(res[i].get('name'), res[i].get('content')) + edit_task.format(res_cnt)
                res_cnt += 1
            except IndexError:
                break
    else:
        offset = callback_data.offset
        res_text = empty_todo_list

    await callback.answer()

    if offset != callback_data.offset or callback_data.act == 'list':
        params = {'doer_id': callback.from_user.id, 'offset': offset, 'limit': limit}
        buttons_acts = ('<<', '>>', 'MENU')
        kb = get_inline_kb(width=len(buttons_acts) - 1, *buttons_acts, **params)
        del_msg = await callback.message.answer(text=res_text, reply_markup=kb)
        await callback.message.delete()
        await state.update_data({'msg': del_msg.message_id})
    await state.set_state(FSMTodoEdit.edit)






