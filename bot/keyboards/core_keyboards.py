from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.filters.callback_factory import CallbackFactorySeaBattle

def get_inline_kb(width: int = 1, *args, factory = None, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if factory:
        for btn, txt in kwargs.items():
            button = InlineKeyboardButton(text=txt, callback_data=CallbackFactorySeaBattle(x=btn[0], y=btn[1]).pack())
            buttons.append(button)
    elif args:
        for button in args:
            buttons.append(InlineKeyboardButton(text= button, callback_data= button))

    elif kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
