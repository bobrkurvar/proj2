from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Any, Callable, Awaitable
import logging

log = logging.getLogger(__name__)

class InCachePageMiddleware(BaseMiddleware):
    # Мидлварь для пагинцаии списка заданий.
    # До попадание в хандлер создаёт в хранилище значения страниц по ключам смещения в базе данных.

    async def __call__(self,
                       handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: dict[str, Any]):

        state, callback_data, ext_api_manager = data.get('state'), data.get('callback_data'), data.get('ext_api_manager')
        pages = (await state.get_data()).get('pages')
        limit = callback_data.limit
        offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
                   '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}

        offset: int = offsets.get(callback_data.act, callback_data.offset)

        # Если ещё не делался запрос в базу - то значения None, а если ответ база пустой то dict()
        if pages is None:
            pages = {}
            try:
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=event.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES IS NONE:')
                pages.update({offset: to_update})
            except TypeError:
                log.error('СПИСОК ЗАДАНИЙ ПУСТ')
        # Если словарь со страницами есть, но текущей страницы там нет
        elif str(offset) not in pages.keys():
            to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=event.from_user.id, limit=limit, offset=offset))
            log.debug('PAGES NOT HAVE OFFSET')
            if not to_update:
                pages.update({offset: None})
            else:
                pages.update({offset: to_update})
        await state.update_data(pages=pages)
        result = await handler(event, data)
        return result

class DeleteUsersMessage(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: dict[str, Any]):
        result = await handler(event, data)
        await event.delete()
        return result
