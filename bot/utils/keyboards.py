import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.filters.callback_factory import CallbackFactoryTodo

log = logging.getLogger(__name__)


def get_inline_kb(
    *button_texts, width: int = 1, buttons_data_lst: list = None, **button_data
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    log.debug("ids: %s", buttons_data_lst)
    for index, i in enumerate(button_texts):
        if not buttons_data_lst:
            data = dict(button_data)
            data.setdefault("act", i)
            button = InlineKeyboardButton(
                text=i, callback_data=CallbackFactoryTodo(**data).pack()
            )
        else:
            try:
                data = buttons_data_lst[index]
            except IndexError:
                data = {}
            data.setdefault("act", i)
            old_data = dict(button_data)
            old_data.pop("id", None)
            data.update(**old_data)
            button = InlineKeyboardButton(
                text=i, callback_data=CallbackFactoryTodo(**data).pack()
            )
        buttons.append(button)
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
