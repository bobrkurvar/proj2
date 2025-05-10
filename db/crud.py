from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.exceptions import CustomException

class Crud:
    def __init__(self, url):
        self._engine = create_async_engine(url)
        self._session = async_sessionmaker(self._engine)

    async def create(self, model, **kwargs):
        try:
            async with self._session.begin() as session:
                print(kwargs)
                tup = model(**kwargs)
                session.add(tup)
        except IntegrityError as err:
            raise CustomException(message=' '.join(err.detail),
                                  detail=' '.join(err.detail))

    async def delete(self, model, ident):
        try:
            async with self._session.begin() as session:
                for_remove = await session.get(model, ident)
                await session.delete(for_remove)
        except UnmappedInstanceError:
            return ident

    async def update(self, model, ident, **kwargs):
        async with self._session.begin() as session:
            for_update = await session.get(model, ident)
            if for_update:
                for atr, val in kwargs.items():
                    for_update.__setattr__(atr, val)

    async def read(self, model, indent: tuple, limit: int = None, offset: int = None):
        async with self._session.begin() as session:
            query = select(model).where(getattr(model, indent[0]) == indent[1])
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            res = (await session.execute(query)).scalars()
            return [r.to_dict() for r in res]

    async def close_and_dispose(self):
        await self._engine.dispose()


if __name__ == "__main__":
    import asyncio
    from db.models import User
    from core import conf
    async def main():
        manager = Crud(str(conf.DATABASE_URL))
        res = await manager.read(User, ('activity', True))
        print(res)

    asyncio.run(main())
