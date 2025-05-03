from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.core_keyboards import get_inline_kb
from bot.lexicon.core_lexicon import START_LEXICON, GAMES_BTN_LEXICON
from bot.utils import get_session_manager
from db.models import User

router = Router(name="command_start")

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    user = {"id": message.from_user.id, "first_name": message.from_user.first_name, "last_name": message.from_user.last_name, "activity": True}
    api_manager = await get_session_manager()
    await api_manager.register_for_bot(**user)
    keyboard = get_inline_kb(width=2,**GAMES_BTN_LEXICON)
    await message.answer(text = START_LEXICON["start_msg"],
                         reply_markup=keyboard)
    await message.delete()

@router.message(Command(commands=['end']))
async def process_remove_from_db_command(message: Message):
    api_manager = await get_session_manager()
    param = {"user_id": message.from_user.id}
    await api_manager.remove_from_bot(**param)
    await message.delete()

