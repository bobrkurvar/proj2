import asyncio
from aiogram import Bot
from datetime import date
from bot.utils.keyboards import get_inline_kb
from aiogram.fsm.context import FSMContext


def leap_year(year: int):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False

def time_mnt(mnt: int, year: int) -> int:
    time_mnt_start = 0
    for i in range(1, mnt):
        if i in (1,3,5,7,8,10,12):
            time_mnt_start += 31
        elif i in (4,6,9,11):
            time_mnt_start += 30
        elif i == 2:
            i += 29 if leap_year(year) else 28
    return time_mnt_start*24*3600

def time_year(year: int) -> int:
    time_year_start = 0
    for i in range(year):
        time_year_start += 366 if leap_year(i) else 365
    return time_year_start*24*3600

async def send_later(bot: Bot, chat_id: int, start: date | list, end: date | dict[str,int], text: str, todo_id: int):
    time_day_start = start.day*24*3600
    time_mnt_start = time_mnt(start.month, start.year)
    time_year_start = time_year(start.year)
    time_start = time_day_start + time_mnt_start + time_year_start
    time_day_end = end['day']*24*3600
    time_mnt_end = time_mnt(end['month'], end['year'])
    time_year_end = time_year(end['year'])
    time_end = time_day_end + time_mnt_end + time_year_end
    time = time_end - time_start
    await asyncio.sleep(3)
    buttons = ('delete', 'complete', 'change deadline')
    kb = get_inline_kb(*buttons, width=3, id=todo_id)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=kb)

async def delete_messages(bot: Bot, chat_id: int, message_id: int, timeout: int, state: FSMContext):
    task = (await state.get_data()).get('prev_back_task')
    if task:
        try:
            await task.cancel()
        except:
            pass
    #await state.update_data(message_delete=message_id)
    await asyncio.sleep(timeout)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

# async def make_task_delete_messages(bot: Bot, chat_id: int, message_id: int, timeout: int, state: FSMContext):
#     tasks = []
#     while True:
#         task = asyncio.create_task(delete_messages(bot, chat_id, message_id, timeout, state))
#         if task in tasks:
#             try:
#                 task.cancel()
#             except:
#                 pass
#         else:
#             tasks.append(task)
#         await task
#         await state.update_data(prev_back_task=task)
#         await asyncio.sleep(timeout)



