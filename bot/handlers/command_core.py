from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from bot.lexicon import start, _help
from bot.keyboards.core_keyboards import get_inline_for_start_kb
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.utils import get_external_api_session_manager, MyExternalApiForBot
from bot.lexicon import _help

router = Router(name="command_start")

@router.message(CommandStart(), StateFilter(default_state))
async def process_command_start(message: Message):
    manager: MyExternalApiForBot = await get_external_api_session_manager('user')
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await manager.create(**user)
    user_id = message.from_user.id
    kb = get_inline_for_start_kb(user_id)
    await message.answer(text=start, reply_markup=kb)
    await message.delete()

@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_state_command(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()

@router.message(StateFilter(default_state))
async def process_delete_unknown(message: Message):
    await message.delete()
    await message.answer(text=_help)
