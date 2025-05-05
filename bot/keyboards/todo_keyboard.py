from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.filters.callback_factory import CallbackFactoryTodo

def get_inline_kb_current_task(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for i in ('<<', 'EDIT', '>>'):
        kwargs.setdefault('offset', 0)
        if i == '<<':
            kwargs['offset'] -= 1 if kwargs['offset'] > 0 else 0
        elif i == '>>':
            kwargs['offset'] += 1
        button = InlineKeyboardButton(text=i, callback_data=CallbackFactoryTodo(act = i, **kwargs).pack())
        buttons.append(button)
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()



