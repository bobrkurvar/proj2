from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot.utils.keyboards import get_inline_kb
from bot.lexicon import phrases
from bot.filters.states import FSMTodoFill, FSMTodoEdit
from bot.utils import MyExternalApiForBot
from bot.utils.handlers import to_date_dict
from bot.filters.custom_filters import IsDate

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act == 'create'), StateFilter(default_state))
async def process_create_task(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    kb = get_inline_kb('menu')
    await callback.message.edit_text(text=phrases.fill_todo_name, reply_markup=kb)
    await state.set_state(FSMTodoFill.fill_name)


@router.message(StateFilter(FSMTodoFill.fill_name))
async def process_create_task_name(message: Message, state: FSMContext):
    msg = (await state.get_data()).get('msg')
    kb = get_inline_kb('menu')
    await state.update_data(name=message.text)
    await message.delete()
    await message.bot.edit_message_text(chat_id = message.chat.id, message_id=msg, text=phrases.fill_todo_content, reply_markup=kb)
    await state.set_state(FSMTodoFill.fill_content)


@router.message(StateFilter(FSMTodoFill.fill_content))
async def process_create_task_content(message: Message, state: FSMContext):
    msg = (await state.get_data()).get('msg')
    kb = get_inline_kb('menu')
    await message.delete()
    await state.update_data(content=message.text)
    await message.bot.edit_message_text(chat_id = message.chat.id, message_id=msg, text=phrases.fill_todo_deadline, reply_markup=kb)
    await state.set_state(FSMTodoFill.fill_deadline)

@router.message(IsDate(), StateFilter(FSMTodoFill.fill_deadline))
async def process_create_task_deadline_success(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    data = await state.get_data()
    msg = (await state.get_data()).get('msg')
    deadline = to_date_dict(message.text)
    del data['msg']
    data.update(doer_id=message.from_user.id, deadline=deadline)
    buttons_text = 'menu'
    kb = get_inline_kb(buttons_text, doer_id=message.from_user.id, limit=3)
    await ext_api_manager.create('todo', **data)
    await message.bot.edit_message_text(chat_id = message.chat.id, message_id=msg, text=phrases.created_todo, reply_markup=kb)
    await message.delete()
    await state.clear()

@router.message(StateFilter(FSMTodoFill.fill_deadline))
async def process_create_task_deadline_fail(message: Message, state: FSMContext):
    msg = (await state.get_data()).get('msg')
    await message.bot.edit_message_text(chat_id=message.chat.it, message_id=msg, text=phrases.fail_fill_deadline)
    await message.delete()

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower().in_({'name', 'content', 'deadline'})), StateFilter(FSMTodoEdit.edit))
async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo,state: FSMContext):
    await callback.answer()
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
    msg = await callback.message.edit_text(text=f'<b>ВВЕДИТЕ НОВОЕ {data_of_edit[callback_data.act.lower()]}</b>\n\n')
    await state.update_data(msg=msg.message_id, updating_data=callback_data.act.lower())
    await state.set_state(edit_states.get(callback_data.act.lower()))


@router.message(StateFilter(FSMTodoEdit.edit_date), IsDate())
@router.message(StateFilter(FSMTodoEdit.edit_name, FSMTodoEdit.edit_content))
async def process_edit_todo(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    data_from_fsm = await state.get_data()
    current_task = data_from_fsm.get('cur_task')
    task_id = current_task.get('id')
    updating_data_name = data_from_fsm.get('updating_data')
    updating_data_content = to_date_dict(message.text) if updating_data_name == 'deadline' else message.text
    updating_data = {updating_data_name: updating_data_content, 'ident_val': task_id}
    await ext_api_manager.update('todo', **updating_data)
    params = dict(limit=3, offset=0)
    buttons = 'menu'
    kb = get_inline_kb(buttons, **params)
    msg = (await state.get_data()).get('msg')
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg, text=phrases.start, reply_markup=kb)
    (await state.get_data()).pop('msg')
    await message.delete()
    await state.clear()

@router.message(StateFilter(FSMTodoEdit.edit_date))
async def process_fail_edit_deadline(message: Message, state: FSMContext):
    bot_message_id = (await state.get_data())['msg']
    send_message = await message.answer(text=phrases.fail_fill_deadline)
    await state.update_data(msg=send_message.message_id)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = bot_message_id)
    await message.delete()


@router.message(StateFilter(FSMTodoEdit.edit))
async def delete_misplaced_message(message: Message):
    await message.delete()








