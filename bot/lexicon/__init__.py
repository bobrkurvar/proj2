
from . import core_lexicon
from . import lexicon

__all__ = ["start", "_help", "fill_todo_name", "fill_todo_content", "created_todo"]

start = core_lexicon.CORE_LEXICON["start"]
_help = core_lexicon.CORE_LEXICON["help"]
fill_todo_name = lexicon.FILL_TODO_LEXICON["fill_name"]
fill_todo_content = lexicon.FILL_TODO_LEXICON["fill_content"]
created_todo = lexicon.FILL_TODO_LEXICON["created"]