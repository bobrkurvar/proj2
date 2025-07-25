from celery import Celery
from celery.schedules import crontab
from bot.utils import ext_api_manager
from main_bot import bot
from datetime import date
from core import conf
from bot.utils.keyboards import get_inline_kb
import asyncio

host = conf.redis_host

app = Celery('celery_tasks', broker=f"redis://{host}:6379/0")
app.conf.beat_schedule = {
    "task-every-hour": {
        "task": "services.celery_tasks.task_hourly",  # путь к первой задаче
        "schedule": crontab(minute='*'),  # каждый час в 00 минут
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
    todos = await ext_api_manager.read(prefix='todo')
    for i in todos:
        if i.get('deadline') == date.today():
            await ext_api_manager.remove(prefix='todo', ident='id', ident_val=i.get('id'))
            kb = get_inline_kb('close')
            doer_id = i.get('doer_id')
            task_id = i.get('id')
            await bot.send_message(chat_id=doer_id, text=f'время задания {task_id} истекло', reply_markup=kb)

async def _task_delete_message():
    messages = await ext_api_manager.read(prefix='message')
    for i in messages:
        try:
            await bot.delete_message(i.get('user_id'), i.get('id'))
        except:
            pass
    await ext_api_manager.remove(prefix='message')


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
