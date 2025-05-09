from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.filters.callback_factory import CallbackFactoryTodo

def get_inline_for_start_kb(ident, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for i in ('list', 'create', 'remove'):
        button = InlineKeyboardButton(text = i, callback_data=CallbackFactoryTodo(act=i, doer_id=ident).pack())
        buttons.append(button)
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()

