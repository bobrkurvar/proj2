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
from bot.filters.states import FSMTodoEdit, FSMTodoFill
from core import logger

router = Router(name="command_start")

@router.message(CommandStart(), StateFilter(default_state))
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot, state: FSMContext):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await ext_api_manager.create(prefix = 'user', **user)
    buttons = ('list', 'create')
    limit = 3
    try:
        lst_todo = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=message.from_user.id, limit=limit))
        print('-' * 100, lst_todo, '-' * 100, sep='\n')
    except TypeError:
        lst_todo = list()
    await state.set_data({'task_list':lst_todo})
    kb = get_inline_kb(*buttons, doer_id=message.from_user.id, limit=limit)
    del_msg = (await state.get_data()).get('del_help_msg', None)
    if not (del_msg is None):
        await message.bot.delete_message(chat_id=message.chat.id, message_id=del_msg)
    await message.delete()
    await message.answer(text=phrases.start, reply_markup=kb)

@router.message(Command(commands=['help']),StateFilter(default_state))
async def process_delete_unknown(message: Message, state: FSMContext):
    await message.delete()
    del_help_msg = await message.answer(text=phrases.help)
    await state.update_data({'del_help_msg': del_help_msg.message_id})

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'menu'), StateFilter(default_state, FSMTodoEdit.edit, FSMTodoFill))
async def process_press_button_menu(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await callback.answer()
    await state.clear()
    limit = callback_data.limit
    try:
        lst_todo = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit))
    except TypeError:
        lst_todo = None
    await state.set_data({'task_list':lst_todo})
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, limit=limit, doer_id=callback.from_user.id)
    await callback.message.edit_text(text=phrases.start, reply_markup=kb)