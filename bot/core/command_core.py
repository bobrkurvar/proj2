from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name="command_start")

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(text='Играем в угадай число?')

# @router.message(Command(commands=['clear', 'reset']))
# async def process_start_command(message: Message):
#     message.from_user.