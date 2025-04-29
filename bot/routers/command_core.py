from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.core_keyboards import get_inline_kb
from bot.lexicon.core_lexicon import START_LEXICON, GAMES_BTN_LEXICON

router = Router(name="command_start")

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    keyboard = get_inline_kb(**GAMES_BTN_LEXICON)
    await message.answer(text = START_LEXICON["start_msg"],
                         reply_markup=keyboard)
    await message.delete()
