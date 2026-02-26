from datetime import date

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


def to_date(str_data: str) -> date | None:
    try:
        day, mnt, year = (int(d) for d in str_data.split("."))
    except ValueError:
        return None
    return date(year=year, month=mnt, day=day)


def to_date_dict(str_data: str) -> dict[str, int] | None:
    try:
        day, mnt, year = (int(d) for d in str_data.split("."))
    except ValueError:
        return None
    return dict(day=day, month=mnt, year=year)


async def safety_delete_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        pass
