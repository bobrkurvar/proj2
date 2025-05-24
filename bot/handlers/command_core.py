from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from bot.lexicon import start, _help
from bot.utils.keyboards import get_inline_kb
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.utils import MyExternalApiForBot
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.filters.states import FSMTodoEdit

router = Router(name="command_start")

@router.message(CommandStart(), StateFilter(default_state))
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    print(user)
    await ext_api_manager.create(prefix = 'user', **user)
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, doer_id=message.from_user.id, limit=3)
    await message.answer(text=start, reply_markup=kb)
    await message.delete()

@router.message(CommandStart(), ~StateFilter(default_state))
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot,
                                bot: Bot, state: FSMContext):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await ext_api_manager.create(prefix='user', **user)
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, doer_id=message.from_user.id, limit=3)
    await message.answer(text=start, reply_markup=kb)
    del_msg = (await state.get_data()).get('del_msg')
    await bot.delete_message(message.chat.id, del_msg)
    await message.delete()

@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_state_command(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()

@router.message(Command(commands=['help']),StateFilter(default_state))
async def process_delete_unknown(message: Message):
    await message.delete()
    await message.answer(text=_help)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'menu'), StateFilter(default_state, FSMTodoEdit.edit))
async def process_press_button_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, limit=3)
    await callback.message.answer(text=start, reply_markup=kb)
    await callback.message.delete()
    await state.clear()