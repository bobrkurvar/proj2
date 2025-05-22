import asyncio
from aiogram import Bot

async def send_later(bot: Bot, chat_id: int, time: int = 10):
    await asyncio.sleep(time)
    await bot.send_message(chat_id, 'hello timer')
