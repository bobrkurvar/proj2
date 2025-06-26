from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot.utils.keyboards import get_inline_kb
from bot.lexicon import phrases
from bot.filters.states import FSMTodoFill, FSMTodoEdit, FSMSearch
from bot.utils import MyExternalApiForBot
from bot.utils.middleware import InCachePageMiddleware
from bot.utils.handlers import to_date_dict
from bot.filters.custom_filters import IsDate

router = Router()
router.callback_query.middleware(InCachePageMiddleware())

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'create'})), StateFilter(default_state))
async def process_create_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    kb = get_inline_kb('MENU')
    msg = (await callback.message.edit_text(text=phrases.fill_todo_name, reply_markup=kb)).message_id
    await state.update_data(msg=msg, offset=callback_data.offset)
    await state.set_state(FSMTodoFill.fill_name)


@router.message(StateFilter(FSMTodoFill.fill_name))
async def process_create_task_name(message: Message, state: FSMContext):
    kb = get_inline_kb('MENU')
    msg = (await state.get_data()).get('msg')
    msg = (await message.bot.edit_message_text(message_id=msg, chat_id=message.chat.id, text=phrases.fill_todo_content, reply_markup=kb)).message_id
    await state.update_data(msg=msg, name=message.text)
    await state.set_state(FSMTodoFill.fill_content)


@router.message(StateFilter(FSMTodoFill.fill_content))
async def process_create_task_content(message: Message, state: FSMContext):
    kb = get_inline_kb('MENU')
    msg = (await state.get_data()).get('msg')
    msg = (await message.bot.edit_message_text(message_id=msg, chat_id=message.chat.id, text=phrases.fill_todo_deadline, reply_markup=kb)).message_id
    await state.update_data(msg=msg, content=message.text)
    await state.set_state(FSMTodoFill.fill_deadline)

@router.message(IsDate(), StateFilter(FSMTodoFill.fill_deadline))
async def process_create_task_deadline_success(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    data = await state.get_data()
    deadline = to_date_dict(message.text)
    to_update = dict(doer_id=message.from_user.id, deadline=deadline, content=data.pop('content'), name=data.pop('name'))
    kb_data = dict(doer_id=message.from_user.id)
    msg = data.get('msg')
    kb = get_inline_kb('MENU', **kb_data)
    await ext_api_manager.create('todo', **to_update)
    msg = (await message.bot.edit_message_text(message_id = msg, chat_id=message.chat.id, text=phrases.created_todo, reply_markup=kb)).message_id
    pages = data.get('pages')
    offset = max(pages.keys())
    if pages.get(str(offset)) is None:
        if len(pages.get(str(offset-3))) < 3:
            offset -= 3
    pages.pop(str(offset))
    data.update(msg=msg, pages=pages)
    await state.clear()
    await state.update_data(data)

@router.message(StateFilter(FSMTodoFill.fill_deadline))
async def process_create_task_deadline_fail(message: Message, state: FSMContext):
    msg = (await state.get_data()).get('msg')
    kb = get_inline_kb('MENU')
    msg = (await message.bot.edit_message_text(message_id=msg, chat_id=message.chat.id, text=phrases.fail_fill_deadline, reply_markup=kb)).message_id
    await state.update_data(msg=msg)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower().in_({'name', 'content', 'deadline'})), StateFilter(FSMTodoEdit.edit))
async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo,state: FSMContext):
    data_of_edit = {
        'name': 'ИМЯ',
        'content': 'СОДЕРЖАНИЕ',
        'deadline': 'ВРЕМЯ ВЫПОЛНЕНИЯ',
    }
    edit_states = {
        'name': FSMTodoEdit.edit_name,
        'content': FSMTodoEdit.edit_content,
        'deadline': FSMTodoEdit.edit_date,
    }
    msg = (await callback.message.edit_text(text=f'<b>ВВЕДИТЕ НОВОЕ {data_of_edit[callback_data.act.lower()]}</b>\n\n')).message_id
    await state.update_data(msg=msg, updating_data=callback_data.act.lower())
    await state.set_state(edit_states.get(callback_data.act.lower()))


@router.message(StateFilter(FSMTodoEdit.edit_date), IsDate())
@router.message(StateFilter(FSMTodoEdit.edit_name, FSMTodoEdit.edit_content))
async def process_edit_todo(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    state_data= await state.get_data()
    current_task = state_data.pop('cur_task')
    task_id = current_task.get('id')
    updating_data_name = state_data.pop('updating_data')
    updating_data_content = to_date_dict(message.text) if updating_data_name == 'deadline' else message.text
    updating_data = {updating_data_name: updating_data_content, 'ident_val': task_id}
    await ext_api_manager.update('todo', **updating_data)
    kb_data = dict(limit=3, offset=0)
    kb = get_inline_kb('MENU', **kb_data)
    pages = state_data.get('pages')
    offset = max(pages.keys())
    if pages.get(str(offset)) is None:
        if len(pages.get(str(int(offset)-3))) < 3:
            offset = str(int(offset) - 3)
    pages.pop(str(offset))
    msg = (await state.get_data()).get('msg')
    msg = (await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg, text=phrases.start, reply_markup=kb)).message_id
    state_data.update(msg=msg, pages=pages)
    await state.clear()
    await state.update_data(state_data)

@router.message(StateFilter(FSMTodoEdit.edit_date))
async def process_fail_edit_deadline(message: Message, state: FSMContext):
    msg = (await state.get_data()).get('msg')
    kb = get_inline_kb('MENU')
    msg = (await message.bot.edit_message_text(message_id=msg, chat_id=message.chat.id, text=phrases.fail_fill_deadline, reply_markup=kb)).message_id
    await state.update_data(msg=msg)

@router.callback_query(StateFilter(FSMSearch.filter), CallbackFactoryTodo.filter(F.act.lower().in_({'name', 'content', 'deadline'})))
async def process_select_criterion(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    data_of_edit = {
        'name': 'ИМЯ',
        'content': 'СОДЕРЖАНИЕ',
        'deadline': 'ВРЕМЯ ВЫПОЛНЕНИЯ',
    }
    edit_states = {
        'name': FSMSearch.filter_by_name,
        'content': FSMSearch.filter_by_content,
        'deadline': FSMSearch.filter_by_deadline,
    }
    msg = (await callback.message.edit_text(text=f'<b>ВВЕДИТЕ {data_of_edit[callback_data.act.lower()]} для поиска</b>\n\n')).message_id
    await state.update_data(msg=msg, filter_data=callback_data.act.lower())
    await state.set_state(edit_states.get(callback_data.act.lower()))

@router.message(StateFilter(FSMSearch.filter_by_deadline), IsDate())
@router.message(StateFilter(FSMSearch.filter_by_name, FSMSearch.filter_by_content))
async def process_search_by_criterion(message: Message, state: FSMContext):
    data = await state.get_data()
    filter_data_name = data.pop('filter_data')
    filter_data = to_date_dict(message.text) if filter_data_name == 'deadline' else message.text

    if isinstance(filter_data, dict):
        filter_data = f'{filter_data.get('year')}-{filter_data.get('mounth')}-{filter_data.get('day')}'

    pages = data.get('pages')
    match = list()

    for i in pages:
        for j in pages.get(i):
            if j.get(filter_data_name) == filter_data:
                match.append(j)

    if match:
        text = ' '
        for i in match:
            text += phrases.list_todo_view.format(i.get('name'), i.get('content'), i.get('deadline'))

        if text == ' ':
            text = phrases.empty_todo_list

        kb_data = dict(width = 1)
        kb = get_inline_kb('MENU', **kb_data)

        msg = data.get('msg')
        try:
            msg = (await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg, text=text, reply_markup=kb)).message_id
            await state.update_data(msg=msg)
        except TelegramBadRequest:
            pass

    await state.clear()
    await state.update_data(data)









