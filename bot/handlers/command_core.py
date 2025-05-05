from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from bot.lexicon import start, _help
from bot.keyboards.core_keyboards import get_inline_for_start_kb

router = Router(name="command_start")

@router.message(CommandStart())
async def process_command_start(message: Message):
    user_id = message.from_user.id
    kb = get_inline_for_start_kb(user_id)
    await message.answer(text=start, reply_markup=kb)

@router.message(Command(commands=["help",]))
async def process_unknown_command(message: Message):
    await message.answer(text=_help)

