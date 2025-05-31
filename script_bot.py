from core import conf, logger
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from bot.handlers import main_router
import asyncio
from bot.utils import ext_api_manager

async def main():
    try:
        bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        await ext_api_manager.connect()
        dp['ext_api_manager'] = ext_api_manager
        dp.include_router(main_router)
        logger.debug('НАЧАЛО РАБОТЫ БОТА')
        await dp.start_polling(bot)
    finally:
        try:
            if ext_api_manager:
                await ext_api_manager.close()
            print(100*'-', 'ЗАКРЫТИЕ СОЕДИНЕНИЯ ВНЕШНЕГО API', 100*'-', sep='\n')
        except Exception:
            logger.info('ПОДКЛЮЧЕНИЕ НЕ БЫЛО ЗАКРЫТО')

if __name__ == "__main__":
    asyncio.run(main())