from core import conf, logger
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from bot.handlers import core_handler, todo_handler, todo_with_state_handler
import asyncio
from bot.utils import get_ext_api_manager

async def main():
    try:
        bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        ext_api_manager = await get_ext_api_manager()
        dp['ext_api_manager'] = ext_api_manager
        dp['list_id'] = []
        dp.include_router(core_handler)
        dp.include_router(todo_handler)
        dp.include_router(todo_with_state_handler)
        logger.info('НАЧАЛО РАБОТЫ БОТА')
        await dp.start_polling(bot)
    finally:
        try:
            await ext_api_manager.close()
            logger.info('ЗАКРЫТИЕ СОЕДИНЕНИЯ ВНЕШНЕГО API')
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())