import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery, Message, User
from aiogram.fsm.context import FSMContext
from bot.lexicon import phrases
from bot.handlers.paginate_todo import process_user_todo_list_button

# @pytest.mark.asyncio
# async def test_process_todo_list_with_tasks():
#     # Моки callback, message, user
#     user = User(id=123, is_bot=False, first_name="Test")
#     message = AsyncMock(spec=Message)
#     message.edit_text.return_value.message_id = 999  # mocked response
#
#     callback = AsyncMock(spec=CallbackQuery)
#     callback.data = "..."  # неважно, мы используем уже распаршенные данные
#     callback.from_user = user
#     callback.message = message
#
#     # Мок callback_data (CallbackFactoryTodo)
#     callback_data = AsyncMock()
#     callback_data.act = '>>'
#     callback_data.limit = 5
#     callback_data.offset = 5
#
#     # Мок FSMContext
#     state = AsyncMock(spec=FSMContext)
#     state.get_data.return_value = {
#         'pages': {
#             '10': [  # offset 10
#                 {'name': 'Задача 1', 'content': 'Описание', 'deadline': '2025-07-22'}
#             ]
#         }
#     }


