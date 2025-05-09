from aiogram.filters.callback_data import CallbackData

class CallbackFactoryTodo(CallbackData, prefix='todo'):
    act: str | None = None
    id: int = 0
    doer_id: int
    offset: int = 0
    limit: int = 1




