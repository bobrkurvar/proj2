from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest
from bot.utils.middleware import InCachePageMiddleware
from bot.utils.keyboards import get_inline_kb
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.lexicon import phrases
from bot.filters.states import FSMTodoEdit, FSMSearch, FSMTodoFill
from bot.utils import MyExternalApiForBot
import logging

router = Router()
router.callback_query.middleware(InCachePageMiddleware())

log = logging.getLogger(__name__)

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})),
                       StateFilter(default_state))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                        state: FSMContext):
    limit = callback_data.limit

    offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
               '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}

    offset: int = offsets[callback_data.act]
    page = (await state.get_data()).get('pages').get(str(offset))
    log.debug('num of page: %s', offset)

    if not (page is None):
        text = ' '

        for i in page:
            text += phrases.list_todo_view.format(i.get('name'), i.get('content'), i.get('deadline'))

        if text == ' ':
            text = phrases.empty_todo_list

        buttons = ['<<', 'EDIT', 'FILTER', 'DELETE', '>>', 'MENU']
        kb_data = dict(offset=offset, limit=limit, doer_id=callback.from_user.id, width=len(buttons)-1)
        kb = get_inline_kb(*buttons, **kb_data)

        try:
            msg = (await callback.message.edit_text(text=text, reply_markup=kb)).message_id
            await state.update_data(msg=msg)
        except TelegramBadRequest:
            pass

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'create'})), StateFilter(default_state))
async def handle_create_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    kb = get_inline_kb('MENU')
    msg = (await callback.message.edit_text(text=phrases.fill_todo_name, reply_markup=kb)).message_id
    await state.update_data(msg=msg, offset=callback_data.offset)
    await state.set_state(FSMTodoFill.fill_name)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower().in_({'filter'})), StateFilter(default_state))
async def handle_filter_button(callback: CallbackQuery, state: FSMContext):
    buttons = ('NAME', 'CONTENT', 'DEADLINE', 'MENU')
    kb = get_inline_kb(*buttons)
    msg = (await callback.message.edit_text(text=phrases.search_criteria, reply_markup=kb)).message_id
    await state.update_data(msg=msg)
    await state.set_state(FSMSearch.filter)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower().in_({'edit'})), StateFilter(default_state))
async def handle_edit_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    res_text = None
    page = (await state.get_data()).get('pages').get(str(callback_data.offset))
    buttons = []
    if page:
        buttons = []
        for i in page:
            buttons.append(i.get('name'))
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')
    kb_data = dict(limit=callback_data.limit, id=callback_data.id, offset=callback_data.offset)
    kb = get_inline_kb(*buttons, **kb_data)
    if not res_text:
        res_text = 'выберете какое задание изменить: '
    msg = (await callback.message.edit_text(text=res_text, reply_markup=kb)).message_id
    await state.update_data(msg=msg)
    await state.set_state(FSMTodoEdit.edit)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'delete'), StateFilter(default_state))
async def handle_delete_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    res_text = None
    log.debug('in delete offset: %s', callback_data.offset)
    pages = (await state.get_data()).get('pages').get(str(callback_data.offset))
    buttons = []
    if pages:
        buttons = []
        for i in pages:
            buttons.append(i.get('name'))
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')
    params = {'limit': callback_data.limit, 'id': callback_data.id}
    kb = get_inline_kb(*buttons, **params)
    if not res_text:
        res_text = 'выберете какое задание удалить: '
    await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.set_state(FSMTodoEdit.delete_task)

@router.callback_query(CallbackFactoryTodo.filter(), StateFilter(FSMTodoEdit.edit, FSMTodoEdit.delete_task))
async def select_task_for_edit(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                     state: FSMContext, ext_api_manager: MyExternalApiForBot):
    data = await state.get_data()
    pages = data.get('pages')
    num = 0
    cur_page = pages.get(str(callback_data.offset))
    for j, i in enumerate(cur_page):
        if i.get('name') == callback_data.act:
            num = j

    cur_task = cur_page[num]
    data.update(cur_task=cur_task)
    buttons = ('NAME', 'CONTENT', 'DEADLINE', 'MENU')
    kb = get_inline_kb(*buttons, width=3)
    text = phrases.process_edit if (await state.get_state()) == FSMTodoEdit.edit else phrases.delete_task.format(cur_page.get('name'))
    msg = (await callback.message.edit_text(text=text, reply_markup=kb)).message_id
    data.update(msg=msg)
    if await state.get_state() == FSMTodoEdit.delete_task:
        data.pop('cur_task')
        await ext_api_manager.remove(prefix='todo', todo_id=cur_task.get('id'))
        offset = callback_data.offset
        if pages.get(str(offset)) is None:
            if len(pages.get(str(int(offset) - 3))) < 3:
                offset = str(int(offset) - 3)
        pages.pop(str(offset))
        data.update(pages=pages)
        await state.clear()
    await state.update_data(data)



















