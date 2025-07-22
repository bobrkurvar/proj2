from celery import Celery
from celery.schedules import crontab
from bot.utils import ext_api_manager
from main_bot import bot, dp
from datetime import date
from bot.utils.keyboards import get_inline_kb
import asyncio
import logging


log = logging.getLogger(__name__)

app = Celery('celery_tasks', broker="redis://localhost:6379/0")
app.conf.beat_schedule = {
    "task-every-hour": {
        "task": "services.celery_tasks.task_hourly",  # путь к первой задаче
        "schedule": crontab(minute=0),  # каждый час в 00 минут
        "args": ()
    },
    "task-every-day": {
        "task": "services.celery_tasks.task_daily",  # путь ко второй задаче
        "schedule": crontab(minute=0, hour=9),  # каждый день в 09:00
        "args": ()
    },
}


async def _task_send_about_delete():
    if ext_api_manager._session is None:
        await ext_api_manager.connect()
    try:
        users = await ext_api_manager.read(prefix='user')
        users_id = [r.get('id') for r in users]
        for i in users_id:
            todo = await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=i)
            for t in todo:
                if t.get('deadline') == date.today():
                    await ext_api_manager.remove(prefix='todo', ident='id', ident_val=t.get('id'))
                    kb = get_inline_kb('close')
                    await bot.send_message(chat_id=i, text=f'время задание {t.get('id')} истекло', reply_markup=kb)
    finally:
        await ext_api_manager.close()

async def _task_delete_message():
    try:
        data = await dp.storage.get_data()
    except:
        return
    msg = data.get('msg')
    if msg:
        bot.delete_message()


@app.task
def task_hourly():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            # Если старый loop закрыт — создать новый
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        # Если нет текущего loop вообще
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_task_send_about_delete())

@app.task
def task_daily():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            # Если старый loop закрыт — создать новый
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        # Если нет текущего loop вообще
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_task_delete_message())
