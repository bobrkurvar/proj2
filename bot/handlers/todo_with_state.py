from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from bot.lexicon import fill_todo_name, fill_todo_content, created_todo
from bot.states.todo_states import FSMTodo
from db import manager
from db.models import Todo

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act == 'create'), StateFilter(default_state))
async def process_create_task(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMTodo.fill_name)
    await callback.message.answer(text=fill_todo_name)
    await callback.answer()


@router.message(StateFilter(FSMTodo.fill_name))
async def process_create_task(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSMTodo.fill_content)
    await message.answer(text=fill_todo_content)


@router.message(StateFilter(FSMTodo.fill_content))
async def process_create_task(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    task = await state.get_data()
    task.update({'doer_id': message.from_user.id})
    await manager.create(Todo, **task)
    await state.clear()
    await message.answer(text=created_todo)

