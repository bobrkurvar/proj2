from aiogram.filters.callback_data import CallbackData

class CallbackFactoryTodo(CallbackData, prefix='todo'):
    id: int
    owner_user: int
    todo_group: int



