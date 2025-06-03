from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from bot.lexicon import phrases
from bot.utils.keyboards import get_inline_kb
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.utils import MyExternalApiForBot
from bot.filters.callback_factory import CallbackFactoryTodo

router = Router(name="command_core")

@router.message(CommandStart())
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot, state: FSMContext):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await ext_api_manager.create(prefix = 'user', **user)
    buttons = ('list', 'create')
    limit = 3
    kb = get_inline_kb(*buttons, doer_id=message.from_user.id, limit=limit, offset=0)
    await message.delete()
    data = await state.get_data()
    msg = data.get('msg')
    if msg:
        try:
            await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg, text=phrases.start, reply_markup=kb)
        except Exception:
            msg = await message.answer(text=phrases.start, reply_markup=kb)
            data.update(msg=msg.message_id)
    else:
        msg = await message.answer(text=phrases.start, reply_markup=kb)
        data.update(msg=msg.message_id)
    await state.clear()
    await state.update_data(data)

@router.message(Command(commands=['help']))
async def process_delete_unknown(message: Message, state: FSMContext):
    await message.delete()
    button = 'START'
    data = await state.get_data()
    kb = get_inline_kb(button)
    msg = data.get('msg')
    if msg:
        try:
            await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg, text=phrases.start, reply_markup=kb)
        except Exception:
            msg = await message.answer(text=phrases.start, reply_markup=kb)
            data.update(msg=msg.message_id)
    else:
        msg = await message.answer(text=phrases.start, reply_markup=kb)
        data.update(msg=msg.message_id)
    await state.clear()
    await state.update_data(data)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower()=='start'))
async def process_button_start(callback: CallbackQuery, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await callback.answer()
    user = {'id': callback.from_user.id, 'first_name': callback.from_user.first_name,
            'last_name': callback.from_user.last_name}
    await ext_api_manager.create(prefix='user', **user)
    buttons = ('list', 'create')
    limit = 3
    lst_todo = (await state.get_data()).get('pages')
    if lst_todo is None:
        try:
            lst_todo = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit))
        except TypeError:
            lst_todo = list()
        await state.update_data(pages=lst_todo)
    kb = get_inline_kb(*buttons, doer_id=callback.from_user.id, limit=limit)
    await callback.message.edit_text(text=phrases.start, reply_markup=kb)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower()=='menu'))
async def process_press_button_menu(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await callback.answer()
    data = await state.get_data()
    await state.clear()
    limit = 3
    await state.update_data(data)
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, limit=limit, doer_id=callback.from_user.id)
    await callback.message.edit_text(text=phrases.start, reply_markup=kb)

@router.message(StateFilter(default_state))
async def process_spam(message: Message):
    await message.delete()