from aiogram.filters.callback_data import CallbackData

class CallbackFactoryTodo(CallbackData, prefix='todo'):
    act: str | None = None
    id: int | None = None
    offset: int = 0
    limit: int = 3




