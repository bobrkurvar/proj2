import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from bot.filters.callback_factory import CallbackFactoryTodo
from bot.filters.states import FSMSearch, FSMTodoEdit, FSMTodoFill
from bot.lexicon import phrases
from bot.utils.keyboards import get_inline_kb
from shared.external import MyExternalApiForBot

router = Router()

log = logging.getLogger(__name__)


@router.callback_query(
    CallbackFactoryTodo.filter(F.act.in_({"list", "<<", ">>"})),
    StateFilter(default_state),
)
async def process_user_todo_list_button(
    callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext
):
    limit = callback_data.limit

    offsets = {
        "list": callback_data.offset,
        ">>": callback_data.offset + limit,
        "<<": callback_data.offset - limit if callback_data.offset > limit else 0,
    }

    offset = offsets[callback_data.act]
    page = (await state.get_data()).get("pages").get(str(offset))
    log.debug("номер страницы в данный момент: %s", offset)
    text = " "
    if page:
        for i in page:
            text += phrases.list_todo_view.format(
                i.get("name"), i.get("content"), i.get("deadline")
            )
    else:
        log.debug("список задач пуст")
        text = phrases.empty_todo_list

    try:
        buttons = (
            ["<<", "EDIT", "FILTER", "DELETE", ">>", "MENU"] if page else ("MENU",)
        )
        kb_data = dict(
            offset=offset,
            limit=limit,
            width=len(buttons) - 1 if len(buttons) > 1 else 1,
        )
        kb = get_inline_kb(*buttons, **kb_data)
        msg = (await callback.message.edit_text(text=text, reply_markup=kb)).message_id
        await state.update_data(msg=msg)
    except TelegramBadRequest:
        pass


@router.callback_query(
    CallbackFactoryTodo.filter(F.act.in_({"create"})), StateFilter(default_state)
)
async def handle_create_button(
    callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext
):
    kb = get_inline_kb("MENU")
    msg = (
        await callback.message.edit_text(text=phrases.fill_todo_name, reply_markup=kb)
    ).message_id
    await state.update_data(msg=msg)
    await state.set_state(FSMTodoFill.fill_name)


@router.callback_query(
    CallbackFactoryTodo.filter(F.act.lower().in_({"filter"})),
    StateFilter(default_state),
)
async def handle_filter_button(callback: CallbackQuery, state: FSMContext):
    buttons = ("NAME", "CONTENT", "DEADLINE", "MENU")
    kb = get_inline_kb(*buttons)
    msg = (
        await callback.message.edit_text(text=phrases.search_criteria, reply_markup=kb)
    ).message_id
    await state.update_data(msg=msg)
    await state.set_state(FSMSearch.filter)


@router.callback_query(
    CallbackFactoryTodo.filter(F.act.lower().in_({"edit", "delete"})),
    StateFilter(default_state),
)
async def handle_delete_button(
    callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext
):
    res_text = None
    log.debug("in delete offset: %s", callback_data.offset)
    pages = (await state.get_data()).get("pages").get(str(callback_data.offset))
    buttons = []
    buttons_ids_lst = []
    if pages:
        buttons = []
        for i in pages:
            buttons.append(i.get("name"))
            buttons_ids_lst.append({"id": i.get("id")})
    else:
        res_text = "список заданий пуст"
    buttons.append("all")
    buttons.append("MENU")
    params = {
        "limit": callback_data.limit,
        "id": callback_data.id,
        "offset": callback_data.offset,
    }
    kb = get_inline_kb(*buttons, buttons_data_lst=buttons_ids_lst, **params)
    if not res_text:
        if callback_data.act.lower() == "delete":
            res_text = "выберете какое задание удалить: "
            await state.set_state(FSMTodoEdit.delete_task)
        else:
            res_text = "выберете какое задание изменить: "
            await state.set_state(FSMTodoEdit.edit_task)
    msg = (await callback.message.edit_text(text=res_text, reply_markup=kb)).message_id
    await state.update_data(msg=msg)


@router.callback_query(
    CallbackFactoryTodo.filter(), StateFilter(FSMTodoEdit.delete_task)
)
async def select_task_for_edit(
    callback: CallbackQuery,
    callback_data: CallbackFactoryTodo,
    state: FSMContext,
    ext_api_manager: MyExternalApiForBot,
):
    data = await state.get_data()
    pages = data.get("pages")
    kb = get_inline_kb("MENU", width=3, offset=callback_data.offset)
    if callback_data.act.lower() == "all":
        log.debug("Удаление всех заданий пользователя")
        await ext_api_manager.remove(prefix="todo")
        data.pop("pages")
    else:
        log.debug("Удаление одного задания")
        await ext_api_manager.remove(prefix=f"todo/{callback_data.id}")
        offset = callback_data.offset
        pages.pop(str(offset))
        data.update(pages=pages)
    msg = (
        await callback.message.edit_text(text=phrases.delete_task, reply_markup=kb)
    ).message_id
    data.update(msg=msg)
    await state.set_state(None)
    await state.set_data(data)


@router.callback_query(
    CallbackFactoryTodo.filter(),
    StateFilter(FSMTodoEdit.edit_task, FSMTodoEdit.delete_task),
)
async def select_task_for_edit(
    callback: CallbackQuery,
    callback_data: CallbackFactoryTodo,
    state: FSMContext,
    ext_api_manager: MyExternalApiForBot,
):
    data = await state.get_data()
    buttons = ("NAME", "CONTENT", "DEADLINE", "MENU")
    kb = get_inline_kb(*buttons, width=3, offset=callback_data.offset)
    await state.set_state(FSMTodoEdit.select_crit)
    msg = (
        await callback.message.edit_text(text=phrases.process_edit, reply_markup=kb)
    ).message_id
    data.update(msg=msg)
    await state.set_data(data)
