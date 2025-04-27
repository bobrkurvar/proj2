from aiogram import Bot, Dispatcher
from core.config import load_config
from bot.routers import game_random
from core import command_core

conf = load_config(".env")
token = conf.BOT_TOKEN
print(token)

bot = Bot(token, delete_messages=True)
dp = Dispatcher()

dp.include_router(command_core.router)
dp.include_router(game_random.router)

if __name__ == '__main__':
    dp.run_polling(bot)