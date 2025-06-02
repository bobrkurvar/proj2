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

router = Router()

@router.callback_query(CallbackFactoryTodo.filter(F.act.in_({'list', '<<', '>>'})),
                       StateFilter(default_state))
async def process_user_todo_list_button(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                        ext_api_manager: MyExternalApiForBot, state: FSMContext):
    await callback.answer()
    limit = 3

    offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
               '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}

    offset: int = offsets[callback_data.act]
    emtpy_lst = (await state.get_data()).get('task_list')

    query_flag = False

    if emtpy_lst is None:
        try:
            emtpy_lst = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
        except TypeError:
            emtpy_lst = list()
        await state.update_data(task_list=emtpy_lst)
        query_flag = True

    send_message = True
    lst_todo_first_id = 0
    if emtpy_lst:
        if callback_data.act == 'list':
            try:
                next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset+limit))
            except TypeError:
                next_page = None
            await state.update_data({'next_page': next_page, 'prev_page': None})

        elif callback_data.act == '>>':
            full_data = await state.get_data()
            cur_page = full_data.get('task_list') if query_flag else full_data.get('next_page')
            if(cur_page):
                try:
                    next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset + limit))
                except TypeError:
                    next_page = None

                prev_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset - limit)) if offset >= limit else None if query_flag else full_data.get('task_list')
                await state.update_data({"prev_page": prev_page, "task_list": cur_page, "next_page": next_page})
            else:
                send_message = False

        elif callback_data.act == '<<':
            full_data = await state.get_data()
            cur_page = full_data.get('task_list') if query_flag else full_data.get('prev_page')
            if cur_page:
                prev_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id,limit=limit, offset=offset - limit)) if offset >= limit else None
                if query_flag:
                    next_page = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset + limit))
                else:
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
        await callback.message.edit_text(text=res_text, reply_markup=kb)


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
    await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.set_state(FSMTodoEdit.edit)

@router.callback_query(CallbackFactoryTodo.filter(F.act.lower() == 'delete'))
async def process_delete_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo, state: FSMContext):
    await callback.answer()
    res_text = None
    task_list = (await state.get_data()).get('task_list')
    buttons = []
    if task_list:
        cur_num = 1
        buttons = []
        for i in task_list:
            buttons.append('task' + str(cur_num) + ' - ' + i.get('name'))
            cur_num += 1
    else:
        res_text = 'список заданий пуст'
    buttons.append('MENU')
    params = {'limit': callback_data.limit, 'id': callback_data.id}
    kb = get_inline_kb(*buttons, **params)
    if not res_text:
        res_text = 'выберете какое задание удалить: '
    await callback.message.edit_text(text=res_text, reply_markup=kb)
    await state.set_state(FSMTodoEdit.delete_task)

@router.callback_query(CallbackFactoryTodo.filter(F.act.startswith('task')))
async def process_edit_selected_task(callback: CallbackQuery, callback_data: CallbackFactoryTodo,
                                     state: FSMContext, ext_api_manager: MyExternalApiForBot):
    await callback.answer()
    num = 0
    for i in range(1, callback_data.limit+1):
        if callback_data.act[4] == str(i):
            num=i-1
            break
    cur_task = (await state.get_data()).get('task_list')[num]
    await state.update_data(cur_task=cur_task)
    if (await state.get_state()) == FSMTodoEdit.edit:
        buttons = ('NAME', 'CONTENT', 'DEADLINE', 'MENU')
        kb = get_inline_kb(*buttons, width=3)
        await callback.message.edit_text(text=phrases.process_edit, reply_markup=kb)
    else:
        buttons = 'MENU'
        kb = get_inline_kb(buttons)
        await ext_api_manager.remove(prefix='todo', ident=callback_data.id)
        await callback.message.edit_text(text=phrases.delete_task.format(cur_task.get('name')), reply_markup=kb)















