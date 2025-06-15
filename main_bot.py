from core import conf, logger
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from redis.asyncio import Redis
from aiogram.enums import ParseMode
from bot.handlers import main_router
from aiogram.fsm.storage.memory import MemoryStorage
from bot.filters.states import CustomRedisStorage
from bot.utils.middleware import SendAnswerOrEdit
import asyncio
from bot.utils import ext_api_manager

log = logging
log.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s')

async def main():
    try:
        bot = Bot(conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        try:
            redis = Redis(host='localhost')
            storage = CustomRedisStorage(redis=redis, state_ttl=3600)
        except:
            log.error('не удалось поключиться к redis, использую MemoryStorage')
            storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        await ext_api_manager.connect()
        dp['ext_api_manager'] = ext_api_manager
        dp['bot'] = bot
        dp.include_router(main_router)
        dp.update.middleware(SendAnswerOrEdit())
        log.debug('НАЧАЛО РАБОТЫ БОТА')
        await dp.start_polling(bot)
    finally:
        try:
            if ext_api_manager:
                await ext_api_manager.close()
            log.debug('ЗАКРЫТИЕ СОЕДИНЕНИЯ ВНЕШНЕГО API')
        except Exception:
            log.error('ПОДКЛЮЧЕНИЕ НЕ БЫЛО ЗАКРЫТО')

if __name__ == "__main__":
    asyncio.run(main())