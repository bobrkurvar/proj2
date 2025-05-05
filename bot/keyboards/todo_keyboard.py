from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

# async def get_todo_keyboard(*args, factory: CallbackData, **kwargs):
#     kb_builder = InlineKeyboardBuilder()
#     buttons: list[InlineKeyboardButton] = []
#     if kwargs:
#         for callback, message in kwargs.items():
#             button = InlineKeyboardButton(text = message, callback_data=factory.pack())
#             buttons.append(button)
#
#     kb_builder.row(*buttons, width=5)
#     return kb_builder.as_markup()


def get_todo_keyboard():
    kb_builder = InlineKeyboardBuilder()
    button_right = InlineKeyboardButton(text='>>', callback_data="next")
    button_left = InlineKeyboardButton(text='<<', callback_data="previous")
    kb_builder.row(button_right, button_left, width=2)
    return kb_builder.as_markup()