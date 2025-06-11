from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Any, Callable, Awaitable
import logging
from bot.utils.keyboards import get_inline_kb

log = logging.getLogger('proj2.middleware')

class InCachePageMiddleware(BaseMiddleware):
    # Мидлварь для пагинцаии списка заданий.
    # До попадание в хандлер создаёт в хранилище значения страниц по ключам смещения в базе данных.

    async def __call__(self,
                       handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: dict[str, Any]):
        callback = event
        # Беру нужные объекты из data
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
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES IN NONE: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('СПИСОК ЗАДАНИЙ ПУСТ')
        # Если словарь со страницами есть, но текущей страницы там нет
        elif str(offset) not in pages.keys():
            try:
                to_update = list(await ext_api_manager.read(prefix='todo', ident='doer_id', ident_val=callback.from_user.id, limit=limit, offset=offset))
                log.debug('PAGES NOT HAVE OFFSET: to_update: %s', to_update)
                pages.update({offset: to_update})
            except TypeError:
                log.error('НЕТ СТРАНИЦЫ С ТАКИМ СМЕЩЕНИЕМ')
                # Если текущая страница выходит за рамки - то она принимает значение None,
                # дабы не делать опять лишние запросы
                pages.update({offset: None})
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

class SendAnswerOrEdit(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]):
        message = event.callback_query.message if event.callback_query else event.message
        state = data.get('state') #сохраняю инфу о message_id из state до того как в handler она отчистится
        msg = (await state.get_data()).get('msg') #передаю в handler
        result = await handler(event, data)
        state_data = await state.get_data() #обновлённая хэндлером инфа из state
        text = state_data.get('text')  #текст ответа
        state_data.pop('text')
        kb_data = state_data.get('kb_data')
        state_data.pop('kb_data')            #инфа для клавиатуры
        buttons = state_data.get('buttons')
        state_data.pop('buttons')
        log.debug("state_data: %s", state_data)
        kb = get_inline_kb(*buttons, **kb_data)
        if msg:
            log.debug('в хранилище сообщение %s', msg)
            if text != message.text:
                try:
                    msg = (await message.edit_text(text=text, reply_markup=kb)).message_id
                except:
                    log.debug('сообщения с id %s уже нет', msg)
                    msg = (await message.answer(text=text, reply_markup=kb)).message_id
        else:
            msg = (await message.answer(text=text, reply_markup=kb)).message_id
            log.debug('отослано сообщение %s', msg)
        state_data.update(msg=msg)
        await state.update_data(state_data)
        return result