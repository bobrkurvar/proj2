from celery import Celery, signals
from . import MyExternalApiForBot
from bot.utils.keyboards import get_inline_kb
import asyncio
from core import conf
import ssl


app = Celery('celery_tasks', broker="redis://localhost:6379/0")
BASE_URL = f"https://api.telegram.org/bot{conf.bot_token}"

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

ext_api_manager = MyExternalApiForBot(BASE_URL)

@signals.worker_init.connect
def connect_ext_api_manager():
    loop.run_until_complete(ext_api_manager.connect())

@signals.worker_shutdown.connect
def close_ext_api_manager():
    loop.run_until_complete(ext_api_manager.close())

@app.task
def task1(chat_id: int, name: str, task_id: int):
    loop.run_until_complete(_task1(chat_id, name, task_id))

def kb_to_dict(kb) -> dict:
    return {
        "inline_keyboard": [
            [{"text": btn.text, "callback_data": btn.callback_data} for btn in row]
            for row in kb.inline_keyboard
        ]
    }

async def _task1(chat_id: int, name: str, task_id: int):
    kb = get_inline_kb("menu", "delete", buttons_data_lst=[{"id": task_id}])
    payload = {
        "chat_id": chat_id,
        "text": f"Дедлайн задачи {name} истёк",
        "reply_markup": kb_to_dict(kb)
    }
    await ext_api_manager.create(prefix="/sendMessage", my_server = False, **payload)
    # async with ClientSession() as session:
    #     async with session.post(BASE_URL+"/sendMessage", json=payload, ssl=ssl_context):
    #         pass