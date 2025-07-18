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
from bot.filters.states import FSMTodoEdit, FSMTodoFill, FSMSearch
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
               '<<': callback_data.offset - limit if callback_data.offset > limit else 0}

    offset = offsets[callback_data.act]
    page = (await state.get_data()).get('pages').get(str(offset))
    log.debug('номер страницы в данный момент: %s', offset)
    text = ' '
    if page:
        for i in page:
            text += phrases.list_todo_view.format(i.get('name'), i.get('content'), i.get('deadline'))
    else:
        text = phrases.empty_todo_list

    try:
        if not (page is None):
            buttons = ['<<', 'EDIT', 'FILTER', 'DELETE', '>>', 'MENU'] if page else ('MENU',)
            kb_data = dict(offset=offset, limit=limit, doer_id=callback.from_user.id,
                           width=len(buttons) - 1 if len(buttons) > 1 else 1)
            kb = get_inline_kb(*buttons, **kb_data)
            msg = (await callback.message.edit_text(text=text, reply_markup=kb)).message_id
            await state.update_data(msg=msg)
    except TelegramBadRequest:
        pass

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'create'})), StateFilter(default_state))
async def handle_create_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    kb = get_inline_kb('MENU')
    msg = (await callback.message.edit_text(text=phrases.fill_todo_name, reply_markup=kb)).message_id
    await state.update_data(msg=msg)
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
    todo_id = callback_data.id
    page = (await state.get_data()).get('pages').get(str(callback_data.offset))
    buttons = []
    if page:
        buttons = []
        for i in page:
            buttons.append(i.get('name'))
        todo_id = [i.get('id') for i in page]
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')

    kb_data = dict(limit=callback_data.limit, id=todo_id, offset=callback_data.offset)
    kb = get_inline_kb(*buttons, **kb_data)
    if not res_text:
        res_text = 'выберете какое задание изменить: '
    msg = (await callback.message.edit_text(text=res_text, reply_markup=kb)).message_id
    await state.update_data(msg=msg)
    await state.set_state(FSMTodoEdit.edit_task)

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
    buttons.append('all')
    buttons.append('MENU')
    params = {'limit': callback_data.limit, 'id': callback_data.id, 'offset': callback_data.offset}
    kb = get_inline_kb(*buttons, **params)
    if not res_text:
        res_text = 'выберете какое задание удалить: '
    await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.set_state(FSMTodoEdit.delete_task)

@router.callback_query(CallbackFactoryTodo.filter(), StateFilter(FSMTodoEdit.edit_task, FSMTodoEdit.delete_task))
async def select_task_for_edit(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                     state: FSMContext, ext_api_manager: MyExternalApiForBot):
    data = await state.get_data()
    pages = data.get('pages')
    cur_page = pages.get(str(callback_data.offset))
    num = 0
    for j, i in enumerate(cur_page):
        if i.get('id') == callback_data.id:
            num = j
    cur_task = cur_page[num]
    data.update(cur_task=cur_task)
    buttons = ('NAME', 'CONTENT', 'DEADLINE', 'MENU') if (await state.get_state()) == FSMTodoEdit.edit_task else ('MENU',)
    kb = get_inline_kb(*buttons, width=3, offset=callback_data.offset)
    text = phrases.process_edit if (await state.get_state()) == FSMTodoEdit.edit_task else phrases.delete_task
    if await state.get_state() == FSMTodoEdit.delete_task:
        data.pop('cur_task')
        if callback_data.act.lower() == 'all':
            log.debug('Удаление всех заданий пользоваетля с id: %s', cur_task.get('doer_id'))
            await ext_api_manager.remove(prefix='todo')
            data.pop('pages')
        else:
            log.debug('Удаление задания с id: %s', cur_task.get('id'))
            await ext_api_manager.remove(prefix='todo', todo_id=cur_task.get('id'))
            offset = callback_data.offset
            pages.pop(str(offset))
            data.update(pages=pages)
        await state.clear()
    else:
        log.debug('Изменение задания с id: %s', cur_task.get('id'))
        await state.set_state(FSMTodoEdit.select_crit)
    msg = (await callback.message.edit_text(text=text, reply_markup=kb)).message_id
    data.update(msg=msg)
    await state.update_data(data)



















