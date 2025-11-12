from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.filters.callback_factory import CallbackFactoryTodo
from bot.lexicon import phrases
from bot.utils.funcs import safety_delete_message
from bot.utils.keyboards import get_inline_kb
from shared.external import MyExternalApiForBot

router = Router(name="command_core")


@router.message(CommandStart())
async def process_command_start(
    message: Message, ext_api_manager: MyExternalApiForBot, state: FSMContext
):
    await ext_api_manager.create(
        prefix="user", id=message.from_user.id, username=message.from_user.username
    )
    data = await state.get_data()
    msg = data.get("msg")
    buttons = ("list", "create")
    kb = get_inline_kb(*buttons)
    if msg:
        await safety_delete_message(message.bot, message.chat.id, msg)
    msg = (await message.answer(text=phrases.start, reply_markup=kb)).message_id
    data.update(msg=msg)
    await state.set_state(None)
    await state.update_data(data)


@router.message(Command(commands=["help"]))
async def process_delete_unknown(message: Message, state: FSMContext):
    buttons = ("START",)
    data = await state.get_data()
    msg = data.get("msg")
    kb = get_inline_kb(*buttons)
    if msg:
        await safety_delete_message(message.bot, message.chat.id, msg)
    msg = (await message.answer(text=phrases.start, reply_markup=kb)).message_id
    data.update(msg=msg)
    await state.set_state(None)
    await state.set_data(data)


@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == "start"))
async def process_button_start(
    callback: CallbackQuery, state: FSMContext, ext_api_manager: MyExternalApiForBot
):
    user = {
        "id": callback.from_user.id,
        "first_name": callback.from_user.first_name,
        "last_name": callback.from_user.last_name,
    }
    await ext_api_manager.create(prefix="user", **user)
    buttons = ("list", "create")
    kb = get_inline_kb(*buttons)
    msg = (
        await callback.message.edit_text(text=phrases.start, reply_markup=kb)
    ).message_id
    await state.update_data(msg=msg)


@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == "menu"))
async def process_press_button_menu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    buttons = ("list", "create")
    kb = get_inline_kb(*buttons)
    msg = (
        await callback.message.edit_text(text=phrases.start, reply_markup=kb)
    ).message_id
    data.update(msg=msg)
    await state.set_state(None)
    await state.set_data(data)
