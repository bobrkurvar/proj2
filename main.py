from core import conf
from fastapi import FastAPI
from app.api.endpoints import user_router, todo_router
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import request_validation_exception_handler, global_exception_handler, custom_exception_handler
from aiogram.client.default import DefaultBotProperties
from app.exceptions.custom_errors import CustomException
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from bot.handlers import core_handler, todo_handler, todo_with_state_handler
import asyncio
from bot.utils import get_session_manager

app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(todo_router, prefix='/todo')

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)

async def main():
    bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(core_handler)
    dp.include_router(todo_handler)
    dp.include_router(todo_with_state_handler)
    api_manager = await get_session_manager()

    await dp.start_polling(bot)
    await dp.shutdown()
    await api_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
