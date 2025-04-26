from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.schemas import user
import random

router = Router(name="game_random")

my_number: int | None = None
user = user.User()

@router.message(F.text.in_({'Да', 'Игра', 'да', 'игра'}))
async def process_game(message: Message):
    if not user.game_is_active:
        global my_number; my_number = random.randint(0,100)
        user.game_is_active = True
        await message.answer(text='Число загадано')
    else:
        await message.answer(text='Число уже загадано')


@router.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if user.game_is_active:
        user.game_is_active = False
        await message.answer(text="Игра остановлена")
    else:
        await message.answer(text="Игра не начата")

@router.message()
async def process_number_gues(message: Message):
    if user.game_is_active:
        try:
            if int(message.text) == my_number:
                user.game_is_active = False
                await message.answer(text='Угадали')
            elif int(message.text) > my_number:
                await message.answer(text='Моё число меньше')
            elif int(message.text) < my_number:
                await message.answer(text='Моё число больше')
        except:
            await message.answer(text='Это не число')
