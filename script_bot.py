from core import conf
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from bot.handlers import core_handler, todo_handler, todo_with_state_handler
import asyncio
from bot.utils import get_external_api_session_manager


async def main():
    bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(core_handler)
    dp.include_router(todo_handler)
    dp.include_router(todo_with_state_handler)
    api_manager = await get_external_api_session_manager()

    await dp.start_polling(bot)
    await dp.shutdown()
    await api_manager.close()

if __name__ == "__main__":
    asyncio.run(main())