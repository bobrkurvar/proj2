from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.filters.callback_factory import CallbackFactoryTodo

# def get_inline_kb_current_task(act:str, **kwargs) -> InlineKeyboardMarkup:
#     kb_builder = InlineKeyboardBuilder()
#     buttons: list[InlineKeyboardButton] = []
#     for i in ('<<', 'EDIT', '>>'):
#         kwargs.setdefault('offset', 0)
#         button = InlineKeyboardButton(text=i, callback_data=CallbackFactoryTodo(act = i, **kwargs).pack())
#         buttons.append(button)
#     kb_builder.row(*buttons, width=3)
#     return kb_builder.as_markup()
#
# def get_inline_kb_edit_task(**kwargs) -> InlineKeyboardMarkup:
#     kb_builder = InlineKeyboardBuilder()
#     buttons: list[InlineKeyboardButton] = []
#     for i in ('EDIT NAME', 'EDIT CONTENT', 'EDIT DATE'):
#         button = InlineKeyboardButton(text = i, callback_data=CallbackFactoryTodo(act=i,**kwargs).pack())
#         buttons.append(button)
#     kb_builder.row(*buttons, width=3)
#     return kb_builder.as_markup()

def get_inline_kb(*button_texts, width:int = 1, **button_data):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for i in button_texts:
        act = button_data.get('act', i)
        button_data.update({'act': act})
        button = InlineKeyboardButton(text = i, callback_data=CallbackFactoryTodo(**button_data).pack())
        buttons.append(button)
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
