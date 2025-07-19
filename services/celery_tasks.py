from celery import Celery
from celery.schedules import crontab
from bot.utils import ext_api_manager
from main_bot import bot
from datetime import date
from bot.utils.keyboards import get_inline_kb
import asyncio
import logging

def get_logger():
    return logging.getLogger(__name__)

app = Celery('celery_tasks', broker="redis://localhost:6379/0")
app.conf.beat_schedule = {
    "task-every-hour": {
        "task": "services.celery_tasks.task",  # путь к задаче
        "schedule": crontab(minute="*"),  # запуск каждый час ровно
        "args": ()
    },
}


async def _task():
    log = get_logger()
    log.debug('background task begin')
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
                    kb = get_inline_kb('menu')
                    await bot.send_message(chat_id=i, text=f'время задание {t.get('id')} истекло', reply_markup=kb)
    finally:
        await ext_api_manager.close()

@app.task
def task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_task())
    finally:
        loop.close()
