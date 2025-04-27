from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db.session import get_connect
from db.models import User

router = Router(name="command_start")

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    async for session in get_connect():
        user = User(id = message.from_user.id, first_name = message.from_user.first_name,
                    last_name = message.from_user.last_name, activity = True)
        session.add(user)
        await message.answer(text='Играем в угадай число?')
