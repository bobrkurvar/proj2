from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from core.config import load_config
from bot.routers import command_core, game_rps
import logging

logger = logging.getLogger(__name__)

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начало работы бота'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/payments',
                   description='Платежи')
    ]
    await bot.set_my_commands(main_menu_commands)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:'
               '{lineno} - {name} - {message}',
        style='{'
    )
    logger.info("Starting bot")
    conf = load_config(".env")
    token = conf.BOT_TOKEN

    bot = Bot(token=token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    logger.info('Connecting routers')

    dp.include_router(command_core.router)
    dp.include_router(game_rps.router)

    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())