from datetime import date
from functools import wraps
from aiogram.fsm.context import FSMContext
from bot.utils import MyExternalApiForBot
from bot.filters.callback_factory import CallbackFactoryTodo
from aiogram.types import CallbackQuery
import logging

log = logging.getLogger('proj.bot.external.handlers')


def to_date(str_data : str) -> date | None:
    try:
        day, mnt, year = (int(d) for d in str_data.split('.'))
    except ValueError:
        return None
    return date(year=year, month=mnt, day=day)

def to_date_dict(str_data: str) -> dict[str, int] | None:
    try:
        day, mnt, year = (int(d) for d in str_data.split('.'))
    except ValueError:
        return None
    return dict(day=day, month=mnt, year=year)

def miss_pages_cache(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, callback_data: CallbackFactoryTodo, ext_api_manager: MyExternalApiForBot, state: FSMContext, *args, **kwargs):
        pages = (await state.get_data()).get('pages')
        limit = callback_data.limit
        offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
                   '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}
        offset: int = offsets[callback_data.act]
        log.debug('offset: %s limit: %s', offset, limit)
        if pages is None:
            pages = {}
            try:
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES IN NONE: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('СПИСОК ЗАДАНИЙ ПУСТ')
                pass

        elif str(offset) not in pages.keys():
            try:
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES NOT HAVE OFFSET: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('НЕТ СТРАНИЦЫ С ТАКИМ СМЕЩЕНИЕМ')
                pages.update({offset: None})
        await state.update_data(pages=pages)
        await func(callback, callback_data, ext_api_manager, state, *args, **kwargs)
    return wrapper

