from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from bot.utils import MyExternalApiForBot, miss_pages_cache

from bot.utils.keyboards import get_inline_kb
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.lexicon import phrases
from bot.filters.states import FSMTodoEdit
import logging

router = Router()

log = logging.getLogger('proj.bot.handlers.todo')

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})),
                       StateFilter(default_state))
@miss_pages_cache
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                        ext_api_manager: MyExternalApiForBot, state: FSMContext):
    await callback.answer()
    limit = callback_data.limit

    offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
               '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}

    offset: int = offsets[callback_data.act]
    log.debug('offset: %s limit: %s', offset, limit)
    pages = (await state.get_data()).get('pages').get(str(offset))
    log.debug('pages: %s', pages)
    text = ' '
    for i in pages:
        text += phrases.list_todo_view.format(i.get('name'), i.get('content'), i.get('deadline'))

    buttons = ['<<', 'EDIT', 'DELETE', '>>', 'MENU']
    params = dict(offset=offset, limit=limit, doer_id=callback.from_user.id)
    kb=get_inline_kb(width=4, *buttons, **params)
    try:
        await callback.message.edit_text(text=text, reply_markup=kb)
    except Exception:
        pass


@router.callback_query(CallbackFactoryTodo.filter(F.act.lower()=='edit'))
@miss_pages_cache
async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    await callback.answer()
    res_text = None
    pages = (await state.get_data()).get('pages').get(callback_data.offset)
    buttons = []
    if pages:
        cur_num = 1
        buttons = []
        for i in pages:
            buttons.append('task'+str(cur_num)+ ' - ' + i.get('name'))
            cur_num += 1
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')
    params = {'limit': callback_data.limit, 'id': callback_data.id, 'offset': callback_data.offset}
    kb = get_inline_kb(*buttons, **params)
    if not res_text:
        res_text = 'выберете какое задание изменить: '
    await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.set_state(FSMTodoEdit.edit)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'delete'))
async def process_delete_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    await callback.answer()
    res_text = None
    pages = (await state.get_data()).get('pages').get(callback_data.offset)
    buttons = []
    if pages:
        cur_num = 1
        buttons = []
        for i in pages:
            buttons.append('task' + str(cur_num) + ' - ' + i.get('name'))
            cur_num += 1
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')
    params = {'limit': callback_data.limit, 'id': callback_data.id}
    kb = get_inline_kb(*buttons, **params)
    if not res_text:
        res_text = 'выберете какое задание удалить: '
    await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.set_state(FSMTodoEdit.delete_task)

@router.callback_query(CallbackFactoryTodo.filter(F.act.startswith('task')))
async def process_edit_selected_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                     state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await callback.answer()
    num = 0
    for i in range(1, callback_data.limit+1):
        if callback_data.act[4] == str(i):
            num=i-1
            break
    cur_task = (await state.get_data()).get('pages').get(callback_data.offset)[num]
    await state.update_data(cur_task=cur_task)
    if (await state.get_state()) == FSMTodoEdit.edit:
        buttons = ('NAME', 'CONTENT', 'DEADLINE', 'MENU')
        kb = get_inline_kb(*buttons, width=3)
        await callback.message.edit_text(text=phrases.process_edit, reply_markup=kb)
    else:
        buttons = 'MENU'
        kb = get_inline_kb(buttons)
        await ext_api_manager.remove(prefix='todo', ident=callback_data.id)
        await callback.message.edit_text(text=phrases.delete_task.format(cur_task.get('name')), reply_markup=kb)















