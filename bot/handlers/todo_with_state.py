from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter

from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot.keyboards.todo_keyboard import get_inline_kb
from bot.lexicon import fill_todo_name, fill_todo_content, created_todo, edit_name, edit_content, delete_task
from bot.states.todo_states import FSMTodoFill, FSMTodoDelete
from bot.utils import MyExternalApiForBot

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
async def process_create_task_content(message: Message, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await message.delete()
    data = await state.get_data()
    bot_message_id = data['msg']
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    data.update(content=message.text)
    data.update(doer_id=message.from_user.id)
    del data['msg']
    print(data)
    await ext_api_manager.create('todo', **data)
    await state.clear()
    buttons_text = ('list', 'create', 'remove')
    kb = get_inline_kb(*buttons_text, doer_id = message.from_user.id)
    await message.answer(text=created_todo, reply_markup=kb)
#
# @router.callback_query(CallbackFactoryTodo.filter(F.data == 'EDIT'), StateFilter(default_state))
# async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo):
#     await callback.answer()
#     params = {'doer_id': callback.from_user.id, 'id': callback_data.id, 'offset': callback_data.offset}
#     buttons_acts =  ('EDIT NAME', 'EDIT CONTENT', 'EDIT DATE')
#     kb = get_inline_kb(*buttons_acts, **params)
#     await callback.message.answer(text=edit_task, reply_markup=kb)
#     await callback.message.delete()

@router.callback_query(CallbackFactoryTodo.filter(F.act == 'remove'), StateFilter(default_state))
async def process_press_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=delete_task)
    await state.set_state(FSMTodoDelete.delete_task)


@router.message(F.text.isdigits(), StateFilter(FSMTodoDelete.delete_task))
async def process_delete_task(message: Message, ext_api_manager: MyExternalApiForBot, state: FSMContext):
    await ext_api_manager.remove('todo', id=message.text)
    await state.set_state(default_state)



