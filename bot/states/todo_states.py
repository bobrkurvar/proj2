from aiogram.fsm.state import StatesGroup, State

class FSMTodo(StatesGroup):
    fill_content = State()
    fill_name = State()