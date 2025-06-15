from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Any, Callable, Awaitable
import logging
from bot.utils.keyboards import get_inline_kb
from aiogram.exceptions import TelegramBadRequest

log = logging.getLogger('proj2.middleware')

class InCachePageMiddleware(BaseMiddleware):
    # Мидлварь для пагинцаии списка заданий.
    # До попадание в хандлер создаёт в хранилище значения страниц по ключам смещения в базе данных.

    async def __call__(self,
                       handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: dict[str, Any]):

        state, callback_data, ext_api_manager = data.get('state'), data.get('callback_data'), data.get('ext_api_manager')
        # Эти хэндлеры не имеют доп. логики
        if callback_data.act.lower() == 'delete' or callback_data.act.lower().startswith('task'):
            return await handler(event,data)

        pages = (await state.get_data()).get('pages')
        limit = callback_data.limit
        offsets = {'list': callback_data.offset, '>>': callback_data.offset + limit,
                   '<<': callback_data.offset - limit if callback_data.offset >= limit else 0}
        offset: int = offsets[callback_data.act]
        log.debug('offset: %s limit: %s', offset, limit)
        # Если ещё не делался запрос в базу - то значения None, а если ответ база пустой то dict()
        if pages is None:
            pages = {}
            try:
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=event.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES IN NONE: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('СПИСОК ЗАДАНИЙ ПУСТ')
        # Если словарь со страницами есть, но текущей страницы там нет
        elif str(offset) not in pages.keys():
            to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=event.from_user.id, limit=limit, offset=offset))
            log.debug('PAGES NOT HAVE OFFSET: to_update: %s', to_update)
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

# class SendAnswerOrEdit(BaseMiddleware):
#     async def __call__(self,
#                        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
#                        event: TelegramObject,
#                        data: dict[str, Any]):
#         state = data.get('state') # сохраняю инфу о message_id из state до того как в handler она отчистится
#         old_data = await state.get_data()
#         result = await handler(event, data)
#         new_data = await state.get_data() #обновлённая хэндлером инфа из state
#         text = new_data.get('text')  #текст ответа
#         new_data.pop('text')
#         kb_data = new_data.get('kb_data')
#         new_data.pop('kb_data')            #инфа для клавиатуры
#         buttons = new_data.get('buttons')
#         new_data.pop('buttons')
#         kb = get_inline_kb(*buttons, **kb_data)
#
#         msg = old_data.get('msg')
#         if event.callback_query:
#             callback = event.callback_query
#             log.debug('event callback_query')
#             if text != callback.message.text:
#                 msg = (await callback.message.edit_text(text=text, reply_markup=kb)).message_id
#
#         elif event.message:
#             message = event.message
#             log.debug('event message')
#             if msg:
#                 try:
#                     await message.bot.delete_message(chat_id=message.chat.id, message_id=msg)
#                 except TelegramBadRequest:
#                     log.debug('сообщение %s нет в чате', msg)
#             msg=(await message.answer(text=text, reply_markup=kb)).message_id
#
#         old_data.update(msg=msg)
#         await state.set_data(old_data)
#         return result