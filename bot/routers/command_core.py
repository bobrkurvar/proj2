from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
# from db.session import get_connect
# from db.models import User
from bot.keyboards.core_keyboards import get_inline_keyboard_for_start
from bot.lexicon.core_lexicon import START_LEXICON

router = Router(name="command_start")

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
        await message.answer(text = START_LEXICON["start_msg"],
                             reply_markup=get_inline_keyboard_for_start())

