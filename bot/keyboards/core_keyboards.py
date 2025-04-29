from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_inline_kb(width: int = 1, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(text= button, callback_data= button))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()