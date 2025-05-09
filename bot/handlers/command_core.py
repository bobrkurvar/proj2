from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from bot.lexicon import start, _help
from bot.keyboards.todo_keyboard import get_inline_kb
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.utils import MyExternalApiForBot

router = Router(name="command_start")

@router.message(CommandStart(), StateFilter(default_state))
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await ext_api_manager.create(prefix = 'user', **user)
    buttons = ('list', 'create', 'remove')
    kb = get_inline_kb(*buttons, doer_id=message.from_user.id)
    await message.answer(text=start, reply_markup=kb)

@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_state_command(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()

@router.message(Command(commands=['help']),StateFilter(default_state))
async def process_delete_unknown(message: Message):
    await message.delete()
    await message.answer(text=_help)
