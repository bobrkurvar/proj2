from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Any, Callable, Awaitable
import logging

log = logging.getLogger('proj2.middleware')

class InCachePageMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]):
        callback = data.get('callback')
        state, callback_data, ext_api_manager = data.get('state'), data.get('callback_data'), data.get('ext_api_manager')
        pages = (await state.get_data()).get('pages')
        limit = callback_data.limit
        offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
                   '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}
        offset: int = offsets[callback_data.act]
        log.debug('offset: %s limit: %s', offset, limit)
        if pages is None:
            pages = {}
            try:
                to_update = list(
                    await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id,
                                               limit=limit, offset=offset))
                log.debug('PAGES IN NONE: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('СПИСОК ЗАДАНИЙ ПУСТ')
                pass

        elif str(offset) not in pages.keys():
            try:
                to_update = list(
                    await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id,
                                               limit=limit, offset=offset))
                log.debug('PAGES NOT HAVE OFFSET: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('НЕТ СТРАНИЦЫ С ТАКИМ СМЕЩЕНИЕМ')
                pages.update({offset: None})
        await state.update_data(pages=pages)
        result = await handler(event, data)
        return result