from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from bot.utils import MyExternalApiForBot

from bot.utils.keyboards import get_inline_kb
from bot.filters.callback_factory import CallbackFactoryTodo
from bot.lexicon import phrases
from bot.filters.states import FSMTodoEdit
from core import logger

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})),
                       StateFilter(default_state, FSMTodoEdit.edit))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                        ext_api_manager: MyExternalApiForBot, state: FSMContext):
    await callback.answer()
    limit = 3

    offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
               '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}

    offset: int = offsets[callback_data.act]
    emtpy_lst = (await state.get_data()).get('task_list')

    send_message = True
    lst_todo_first_id = 0
    if(emtpy_lst):
        if callback_data.act == 'list':
            try:
                next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset+limit))
            except TypeError:
                next_page = None
            await state.update_data({'next_page': next_page})

        elif callback_data.act == '>>':
            full_data = await state.get_data()
            cur_page = full_data.get('next_page')
            if(cur_page):
                prev_page=full_data.get('task_list')
                try:
                    next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset + limit))
                except TypeError:
                    next_page = None
                await state.update_data({"prev_page": prev_page, "task_list": cur_page, "next_page": next_page})
            else:
                send_message = False

        elif callback_data.act == '<<':
            full_data = await state.get_data()
            cur_page = full_data.get('prev_page')
            if(cur_page):
                prev_page = None
                if offset >= limit:
                    prev_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset - limit))
                next_page = full_data.get('task_list')
                await state.update_data({'prev_page': prev_page, "task_list": cur_page, "next_page": next_page})
            else:
                send_message = False
        lst_todo =(await state.get_data()).get('task_list')
        res_text = ''
        lst_todo_first_id = lst_todo[0].get('id')
        for i in lst_todo:
            res_text += phrases.list_todo_view.format(i.get('name'), i.get('content'), i.get('deadline'))
    else:
        res_text = phrases.empty_todo_list

    if send_message:
        buttons_acts = ('<<', 'DELETE', 'EDIT', '>>', 'MENU')
        params = {'doer_id': callback.from_user.id, 'offset': offset, 'limit': limit, 'id':lst_todo_first_id}
        kb = get_inline_kb(width = len(buttons_acts)-1, *buttons_acts, **params)
        msg = await callback.message.edit_text(text=res_text, reply_markup=kb)
        await state.update_data(msg=msg.message_id)


@router.callback_query(CallbackFactoryTodo.filter(F.act.lower()=='edit'))
async def process_edit_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    await callback.answer()
    res_text = None
    task_list = (await state.get_data()).get('task_list')
    buttons = []
    if task_list:
        cur_num = 1
        buttons = []
        for i in task_list:
            buttons.append('task'+str(cur_num)+ ' - ' + i.get('name'))
            cur_num += 1
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')
    params = {'limit': callback_data.limit, 'id': callback_data.id}
    kb = get_inline_kb(*buttons, **params)
    if not res_text:
        res_text = 'выберете какое задание изменить: '
    msg = await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.update_data(msg=msg.message_id)

@router.callback_query(CallbackFactoryTodo.filter(F.act.startswith('task')))
async def process_edit_selected_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                     state: FSMContext):
    await callback.answer()
    print(100*'-', callback_data.act, 100*'-', sep='\n')
    for i in range(callback_data.limit):
        if callback_data.act[4] == str(i):
            await state.update_data(num=i)
            break
    buttons = ('NAME', 'CONTENT', 'DEADLINE', 'MENU')
    kb = get_inline_kb(*buttons, width=3)
    await callback.message.edit_text(text=phrases.process_edit, reply_markup=kb)
    await state.set_state(FSMTodoEdit.edit)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'delete'))
async def process_delete_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo, ext_api_manager: MyExternalApiForBot, state: FSMContext):
    await callback.answer()
    start_to_view = (await state.get_data())











