from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from bot.lexicon import phrases
from aiogram.fsm.context import FSMContext
from bot.utils import MyExternalApiForBot
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.utils.keyboards import get_inline_kb
from aiogram.exceptions import TelegramBadRequest

router = Router(name="command_core")

@router.message(CommandStart())
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot, state: FSMContext):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await ext_api_manager.create(prefix = 'user', **user)
    data = await state.get_data()
    msg = data.get('msg')
    buttons = ('list', 'create')
    kb_data = dict(doer_id=message.from_user.id, limit=3, offset=0)
    kb = get_inline_kb(*buttons, **kb_data)
    if msg:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=msg)
        except TelegramBadRequest:
            pass
    msg = (await message.answer(text=phrases.start, reply_markup=kb)).message_id
    data.update(msg=msg)
    await state.clear()
    await state.update_data(data)

@router.message(Command(commands=['help']))
async def process_delete_unknown(message: Message, state: FSMContext):
    buttons = ('START',)
    await state.update_data(text=phrases.help, kb_data={}, buttons=buttons)
    data = await state.get_data()
    msg = data.get('msg')
    kb_data = dict(doer_id=message.from_user.id, limit=3, offset=0)
    kb = get_inline_kb(*buttons, **kb_data)
    if msg:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=msg)
        except TelegramBadRequest:
            pass
    msg = (await message.answer(text=phrases.start, reply_markup=kb)).message_id
    data.update(msg=msg)
    await state.clear()
    await state.update_data(data)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower()=='start'))
async def process_button_start(callback: CallbackQuery, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    user = {'id': callback.from_user.id, 'first_name': callback.from_user.first_name,
            'last_name': callback.from_user.last_name}
    await ext_api_manager.create(prefix='user', **user)
    buttons = ('list', 'create')
    kb_data = dict(doer_id=callback.from_user.id, limit=3)
    kb = get_inline_kb(*buttons, **kb_data)
    if phrases.start != callback.message.text:
        msg = (await callback.message.edit_text(text=phrases.start, reply_markup=kb)).message_id
        await state.update_data(msg=msg)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower()=='menu'))
async def process_press_button_menu(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    data = await state.get_data()
    buttons = ('list', 'create')
    kb_data = dict(limit=3, doer_id=callback.from_user.id, offset=callback_data.offset)
    kb = get_inline_kb(*buttons, **kb_data)
    if phrases.start != callback.message.text:
        msg = (await callback.message.edit_text(text=phrases.start, reply_markup=kb)).message_id
        data.update(msg=msg)
    await state.clear()
    await state.update_data(data)
