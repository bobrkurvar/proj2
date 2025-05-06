from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter

from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot.keyboards.todo_keyboard import get_inline_kb
from bot.lexicon import fill_todo_name, fill_todo_content, created_todo, edit_name, edit_content
from bot.states.todo_states import FSMTodoFill, FSMTodoEdit
from bot.utils import external_api_manager
from db.models import Todo

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act == 'create'), StateFilter(default_state))
async def process_create_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    sent_message = await callback.message.answer(text=fill_todo_name)
    await state.update_data(msg = sent_message.message_id)
    await state.set_state(FSMTodoFill.fill_name)


@router.message(StateFilter(FSMTodoFill.fill_name))
async def process_create_task_name(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_message_id = data['msg']
    await message.bot.delete_message(chat_id = message.chat.id, message_id=bot_message_id)
    await state.update_data(name=message.text)
    await message.delete()
    sent_message = await message.answer(text=fill_todo_content)
    await state.update_data(msg = sent_message.message_id)
    await state.set_state(FSMTodoFill.fill_content)


@router.message(StateFilter(FSMTodoFill.fill_content))
async def process_create_task_content(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    bot_message_id = data['msg']
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await state.update_data(content=message.text)
    del data['msg']
    await external_api_manager.create(Todo, **data)
    await state.clear()
    buttons_text = ('list', 'create', 'remove')
    kb = get_inline_kb(*buttons_text, doer_id = message.from_user.id)
    await message.answer(text=created_todo, reply_markup=kb)

# @router.callback_query(CallbackFactoryTodo.filter(F.data == 'EDIT NAME'), StateFilter(default_state))
# async def process_init_edit_task_name(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
#     await callback.answer()
#     await callback.message.delete()
#     sent_message = await callback.message.answer(text=edit_name)
#     await state.update_data(msg=sent_message.message_id)
#     await state.set_state(FSMTodoEdit.edit_name)

# @router.message(StateFilter(FSMTodoEdit.edit_name))
# async def process_edit_task_name(message: Message, state: FSMContext):
#     await message.delete()
#     kb =



