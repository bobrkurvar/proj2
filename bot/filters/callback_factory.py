from aiogram.filters.callback_data import CallbackData

class CallbackFactorySeaBattle(CallbackData, prefix='sea_battle'):
    x: int | str
    y: int | str



