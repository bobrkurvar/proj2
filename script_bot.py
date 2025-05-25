from core import conf, logger
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from bot.handlers import main_router
import asyncio
from bot.utils import get_ext_api_manager

async def main():
    try:
        bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        ext_api_manager = await get_ext_api_manager()
        dp['ext_api_manager'] = ext_api_manager
        dp.include_router(main_router)
        logger.debug('НАЧАЛО РАБОТЫ БОТА')
        await dp.start_polling(bot)
    finally:
        try:
            await ext_api_manager.close()
            logger.info('ЗАКРЫТИЕ СОЕДИНЕНИЯ ВНЕШНЕГО API')
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())