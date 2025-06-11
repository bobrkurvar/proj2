from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Any, Callable, Awaitable
import logging

log = logging.getLogger('proj2.middleware')

class InCachePageMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: dict[str, Any]):
        callback = event
        state, callback_data, ext_api_manager = data.get('state'), data.get('callback_data'), data.get('ext_api_manager')
        if callback_data.act.lower() == 'delete' or callback_data.act.lower().startswith('task'):
            return await handler(event,data)

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

        elif str(offset) not in pages.keys():
            try:
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES NOT HAVE OFFSET: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('НЕТ СТРАНИЦЫ С ТАКИМ СМЕЩЕНИЕМ')
                pages.update({offset: None})
        await state.update_data(pages=pages)
        result = await handler(event, data)
        return result

class SendOrEditAnswerMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]):
        result = await handler(event, data)
        state = data.get('state')
        bot: Bot = data.get('bot')
        old_text = data.get('text')
        text = state.get('text')
        kb = data.get('kb')
        msg = (await state.get_data).get('msg')
        if isinstance(event, CallbackQuery):
            await event.message.delete()
        elif isinstance(event, Message):
            await event.delete()
        if msg in None:
            msg = await bot.send_message(chat_id=event.chat.id, text=text, reply_markup=kb)
        else:
            if text != old_text:
                msg = await bot.edit_message_text(chat_id=event.chat.id, text=text,
                                                  message_id=msg, reply_markup=kb)
        await state.update_data(msg=msg)
        return result

