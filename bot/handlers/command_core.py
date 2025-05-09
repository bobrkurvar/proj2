from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from bot.lexicon import start, _help
from bot.keyboards.core_keyboards import get_inline_for_start_kb
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from db import manager
from db.models import User

router = Router(name="command_start")

@router.message(CommandStart(), StateFilter(default_state))
async def process_command_start(message: Message):
    user_id = message.from_user.id
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await manager.create(User, **user)
    kb = get_inline_for_start_kb(user_id)
    await message.answer(text=start, reply_markup=kb)
    await message.delete()

@router.message(Command(commands=["help",]))
async def process_unknown_command(message: Message):
    await message.answer(text=_help)
    await message.delete()

