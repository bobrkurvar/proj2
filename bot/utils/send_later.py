import asyncio
from aiogram import Bot

async def send_later(bot: Bot, chat_id: int, time: int, text: str):
    await asyncio.sleep(time)
    await bot.send_message(chat_id=chat_id, text=text)
