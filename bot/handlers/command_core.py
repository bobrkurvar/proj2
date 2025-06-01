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

router = Router(name="command_start")

@router.message(CommandStart(), StateFilter(default_state))
async def process_command_start(message: Message, ext_api_manager: MyExternalApiForBot, state: FSMContext):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name}
    await ext_api_manager.create(prefix = 'user', **user)
    buttons = ('list', 'create')
    data = await state.get_data()
    cur_page = data.get('task_list')
    limit = 3
    offset = 0
    if cur_page in None:
        prev_page = next_page = None
        try:
            cur_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=message.from_user.id, limit=limit,offset=offset))
        except TypeError:
            cur_page = list()

        if not cur_page:
            try:
                next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=message.from_user.id, limit=limit,offset=offset + limit))
            except TypeError:
                next_page = None

            prev_page = None if offset < limit else list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=message.from_user.id, limit=limit, ffset=offset - limit))

        await state.update_data(task_list=cur_page, prev_page=prev_page, next_page=next_page)

    kb = get_inline_kb(*buttons, doer_id=message.from_user.id, limit=limit)
    await message.delete()
    msg = (await state.get_data()).get('msg')
    if msg:
        await msg.edit_text(text=phrases.start, reply_markup=kb)
    else:
        await message.answer(text=phrases.start, reply_markup=kb)

@router.message(Command(commands=['help']),StateFilter(default_state))
async def process_delete_unknown(message: Message, state: FSMContext):
    await message.delete()
    msg = await message.answer(text=phrases.help)
    await state.update_data(msg=msg)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'menu'), StateFilter(default_state, FSMTodoEdit, FSMTodoFill))
async def process_press_button_menu(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await callback.answer()
    data = await state.get_data()
    cur_page = data.get('task_list')
    await state.clear()
    limit = callback_data.limit
    offset = callback_data.offset
    if cur_page in None:
        prev_page = next_page = None
        try:
            cur_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
        except TypeError:
            cur_page = list()

        if not cur_page:
            try:
                next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset + limit))
            except TypeError:
                next_page = None

            prev_page = None if offset < limit else list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset - limit))

        await state.update_data(task_list=cur_page, prev_page=prev_page, next_page=next_page)
    buttons = ('list', 'create')
    kb = get_inline_kb(*buttons, limit=limit, doer_id=callback.from_user.id)
    await callback.message.edit_text(text=phrases.start, reply_markup=kb)