from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update, delete, asc
from sqlalchemy.exc import IntegrityError
from .exceptions import NotFoundError, AlreadyExistsError
import logging

log = logging.getLogger(__name__)

class Crud:
    _engine = None
    _session = None
    def __init__(self, url):
        if not self.__class__._engine:
            self.__class__._engine = create_async_engine(url)
        if not self.__class__._session:
            self.__class__._session = async_sessionmaker(self._engine)

    async def create(self, model, **kwargs):
        try:
            tup = model(**kwargs)
            async with self._session.begin() as session:
                    session.add(tup)
                    return tup.model_dump()
        except IntegrityError:
            raise AlreadyExistsError(model.__name__, 'id', tup.id)

    async def delete(self, model, ident: str | None = None, ident_val = None):
        async with self._session.begin() as session:
            if not (ident_val is None):
                if ident is None:
                    log.debug('Crud получил запрос на удаление id: %s', ident_val)
                    for_remove = await session.get(model, ident_val)
                    if not (for_remove is None):
                        await session.delete(for_remove)
                        return for_remove.model_dump()
                    else:
                        raise NotFoundError(model.__name__, 'id', ident_val)
                else:
                    log.debug('Crud получил запрос на удаление по параметру %s: %s', ident, ident_val)
                    for_remove = (await session.execute(select(model).where(getattr(model, ident) == ident_val))).scalars().all()
                    if not for_remove:
                        raise NotFoundError(model.__name__, ident, ident_val)
                    for chunk in for_remove:
                        await session.delete(chunk)
                    else:
                        return True
            else:
                models = await session.execute(select(model))
                if models is None:
                    raise NotFoundError(model.__name__)
                await session.execute(delete(model))

    async def update(self, model, ident: str, ident_val: int, **kwargs):
        async with self._session.begin() as session:
            query = update(model).where(getattr(model, ident) == ident_val).values(**kwargs)
            await session.execute(query)

    async def read(self, model, ident: str | None = None, ident_val: int | None = None, limit: int | None = None, offset: int | None = None,
                   order_by: str | None = None):
        async with self._session.begin() as session:
            query = select(model)
            if ident:
                query = query.where(getattr(model, ident) == ident_val)
            if order_by:
                log.debug('сортировка по %s', order_by)
                query = query.order_by(getattr(model, order_by))
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)
            res = (await session.execute(query)).scalars().all()
            if not res:
                log.debug('Возвращаемый список пуст: %s', res)
                raise NotFoundError(model.__name__, ident, ident_val)
            log.debug('Список не пуст: %s', res)
            return [r.model_dump() for r in res]

    async def close_and_dispose(self):
        await self._engine.dispose()

