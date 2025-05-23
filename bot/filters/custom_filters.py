from aiogram.filters import BaseFilter
from aiogram.types import Message
from datetime import date

class IsDate(BaseFilter):
    async def __call__(self, message: Message):
        try:
            day, mnt, year = (int(d) for d in message.text.split('.'))
        except ValueError:
            return False
        if year < date.today().year:
            return False
        elif year == date.today().year and mnt < date.today().month:
            return False
        elif year == date.today().year and mnt == date.today().month and day <= date.today().day:
            return False

        return True
