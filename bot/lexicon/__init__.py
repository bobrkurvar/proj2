from bot.lexicon import core_lexicon
from bot.lexicon import lexicon
from pydantic import BaseModel

class Phrases(BaseModel):
    start: str = core_lexicon.CORE_LEXICON["start"]
    help: str = core_lexicon.CORE_LEXICON["help"]
    fill_todo_name: str = lexicon.FILL_TODO_LEXICON["fill_name"]
    fill_todo_content: str = lexicon.FILL_TODO_LEXICON["fill_content"]
    fill_todo_deadline: str = lexicon.FILL_TODO_LEXICON["fill_deadline"]
    fail_fill_deadline: str = lexicon.FILL_TODO_LEXICON["fail_fill_deadline"]
    created_todo: str = lexicon.FILL_TODO_LEXICON["created"]
    list_todo_view: str  = lexicon.TASK_LIST_VIEW['new_task']
    empty_todo_list: str  = lexicon.TASK_LIST_VIEW['empty_list']
    edit_task: str  = lexicon.EDIT_TASK['edit']
    process_edit: str  = lexicon.EDIT_TASK['process_edit']
    delete_task: str  = lexicon.EDIT_TASK['delete_task']

phrases = Phrases()