from aiogram.filters import BaseFilter
from aiogram.types import Message
from datetime import date
from bot.utils.tasks import leap_year

dict_days = dict()
dict_31 = dict.fromkeys([1,3,5,7,8,10,12], 31)
dict_days.update(dict_31)
dict_30 = dict.fromkeys([4,6,9,11], 30)
dict_days.update(dict_30)


class IsDate(BaseFilter):
    async def __call__(self, message: Message):
        try:
            day, mnt, year = (int(d) for d in message.text.split('.'))
        except ValueError:
            return False

        if year >= 3000:
            return False

        if year < date.today().year or year == date.today().year and mnt < date.today().month or year == date.today().year and mnt == date.today().month and day <= date.today().day:
            return False

        if mnt > 12 or mnt < 1 or day < 0:
            return False

        if mnt==2:
            if leap_year(year):
                return False if day > 29 else True
            else:
                return False if day > 28 else True

        if day > dict_days[mnt]:
            return False

        return True
