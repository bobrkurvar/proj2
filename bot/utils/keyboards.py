from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.filters.callback_factory import CallbackFactoryTodo

# def get_inline_kb(*button_texts, width:int = 1, **button_data) -> InlineKeyboardMarkup:
#     kb_builder = InlineKeyboardBuilder()
#     buttons: list[InlineKeyboardButton] = []
#     for i in button_texts:
#         data = dict(button_data)
#         act = data.get('act', i)
#         data.update({'act': act})
#         button = InlineKeyboardButton(text = i, callback_data=CallbackFactoryTodo(**data).pack())
#         buttons.append(button)
#     kb_builder.row(*buttons, width=width)
#     return kb_builder.as_markup()

def get_inline_kb(*button_texts, width:int = 1, **button_data) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    todo_list = button_data.get('id')
    index = None
    if isinstance(todo_list, list | tuple):
        index = 0
    for i in button_texts:
        data = dict(button_data)
        act = data.get('act', i)
        data.update(act=act)
        if not (index is None):
            data.update(id=data.get('id')[index])
            index += 1 if index < len(todo_list) - 1 else 0
        button = InlineKeyboardButton(text = i, callback_data=CallbackFactoryTodo(**data).pack())
        buttons.append(button)
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()