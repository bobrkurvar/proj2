from aiogram.fsm.state import StatesGroup, State

class FSMTodoFill(StatesGroup):
    fill_content = State()
    fill_name = State()

class FSMTodoEdit(StatesGroup):
    edit_content = State()
    edit_name = State()
    edit_date = State()
    delete_task = State()
