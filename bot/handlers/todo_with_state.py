from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
import asyncio
from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot.utils.keyboards import get_inline_kb
from bot.lexicon import fill_todo_name, fill_todo_content, created_todo, process_edit, start, fill_todo_deadline, fail_fill_deadline
from bot.states.todo_states import FSMTodoFill, FSMTodoEdit
from bot.utils import MyExternalApiForBot
from bot.utils.handlers import to_date_dict
from bot.utils.send_later import send_later
from bot.filters.custom_filters import IsDate
from datetime import date

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act == 'create'), StateFilter(default_state))
async def process_create_task(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    send_message = await callback.message.answer(text=fill_todo_name)
    await callback.message.delete()
    await state.update_data(msg = send_message.message_id)
    await state.set_state(FSMTodoFill.fill_name)


@router.message(StateFilter(FSMTodoFill.fill_name))
async def process_create_task_name(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_message_id = data['msg']
    await state.update_data(name=message.text)
    send_message = await message.answer(text=fill_todo_content)
    await message.delete()
    await message.bot.delete_message(chat_id = message.chat.id, message_id=bot_message_id)
    await state.update_data(msg = send_message.message_id)
    await state.set_state(FSMTodoFill.fill_content)


@router.message(StateFilter(FSMTodoFill.fill_content))
async def process_create_task_content(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_message_id = data['msg']
    send_message = await message.answer(text=fill_todo_deadline)
    await message.delete()
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await state.update_data(content=message.text, msg = send_message.message_id)
    await state.set_state(FSMTodoFill.fill_deadline)

@router.message(IsDate(), StateFilter(FSMTodoFill.fill_deadline))
async def process_create_task_deadline_success(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    data = await state.get_data()
    bot_message_id = data['msg']
    deadline = to_date_dict(message.text)
    del data['msg']
    data.update(doer_id=message.from_user.id, deadline=deadline)
    buttons_text = ('menu', )
    kb = get_inline_kb(*buttons_text, doer_id=message.from_user.id, limit=3)
    todo_id = await ext_api_manager.create('todo', **data)
    print(todo_id)
    send_later_task = asyncio.create_task(send_later(bot=message.bot, chat_id=message.chat.id,
                                                     start=date.today(), end=deadline, text='Время задания итстекло', todo_id=todo_id))
    await message.answer(text=created_todo, reply_markup=kb)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await message.delete()
    await state.clear()

@router.message(StateFilter(FSMTodoFill.fill_deadline))
async def process_create_task_deadline_fail(message: Message, state: FSMContext):
    bot_message_id = (await state.get_data())['msg']
    send_message = await message.answer(text=fail_fill_deadline)
    await state.update_data(msg=send_message.message_id)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = bot_message_id)
    await message.delete()


@router.message(F.text.startswith('/edit_task'), StateFilter(FSMTodoEdit.edit))
async def process_pick_edit_task(message: Message, state: FSMContext, bot: Bot):
    current_task_num = int(message.text[-1])-1
    current_task = (await state.get_data()).get('task_list')[current_task_num]
    await state.update_data({'cur_task': current_task})
    buttons = ('NAME', 'CONTENT', 'DEADLINE')
    kb = get_inline_kb(*buttons, width=3)
    del_msg = (await state.get_data()).get('msg')
    await bot.delete_message(message.chat.id, del_msg)
    await message.delete()
    await message.answer(text = process_edit, reply_markup=kb)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower().in_({'name', 'content', 'deadline'})), StateFilter(FSMTodoEdit.edit))
async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo,state: FSMContext):
    await callback.answer()
    data_of_edit = {
        'name': 'ИМЯ',
        'content': 'СОДЕРЖАНИЕ',
        'dedline': 'ВРЕМЯ ВЫПОЛНЕНИЯ',
    }
    edit_states = {
        'name': FSMTodoEdit.edit_name,
        'content': FSMTodoEdit.edit_content,
        'deadline': FSMTodoEdit.edit_date,
    }
    res_msg = await callback.message.answer(text=f'<b>ВВЕДИТЕ НОВОЕ {data_of_edit[callback_data.act.lower()]}</b>\n\n')
    await callback.message.delete()
    await state.update_data({'del_msg': res_msg.message_id, 'updating_data': callback_data.act.lower()})
    await state.set_state(edit_states.get(callback_data.act.lower()))

@router.message(StateFilter(FSMTodoEdit.edit_name, FSMTodoEdit.edit_content, FSMTodoEdit.edit_date))
async def process_edit_name(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot, bot: Bot):
    data_from_fsm = await state.get_data()
    current_task = data_from_fsm.get('cur_task')
    task_id = current_task['id']
    updating_data_name = data_from_fsm.get('updating_data')
    updating_data = {updating_data_name: message.text}
    updating_data.update({'ident': ('id', task_id)})
    del_msg =data_from_fsm.get('del_msg')
    await bot.delete_message(message.chat.id, del_msg)
    await ext_api_manager.update('todo', **updating_data)
    await message.delete()
    params = dict(limit=3, offset=0)
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, **params)
    await message.answer(text=start, reply_markup=kb)
    await state.clear()

@router.message(StateFilter(FSMTodoEdit.edit))
async def delete_misplaced_message(message: Message):
    await message.delete()








