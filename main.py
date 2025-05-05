from core import conf
from fastapi import FastAPI
from app.api.endpoints import user_router, todo_router
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import request_validation_exception_handler, global_exception_handler, custom_exception_handler
from app.exceptions.custom_errors import CustomException
from aiogram import Bot, Dispatcher
from bot.handlers import core_router
import asyncio
from bot.utils import get_session_manager

app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(todo_router, prefix='/todo')

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)

async def main():

    bot = Bot(conf.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(core_router)
    api_manager = await get_session_manager()

    await dp.start_polling(bot)
    await dp.shutdown()
    await api_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
