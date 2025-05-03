from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

class Crud:
    def __init__(self, url):
        self._engine = create_async_engine(url)
        self._session = async_sessionmaker(self._engine)

    async def create(self, model, **kwargs):
        try:
            async with self._session.begin() as session:
                tup = model(**kwargs)
                session.add(tup)
                print(kwargs)
        except IntegrityError:
                print(kwargs)

    async def delete(self, model, ident):
        try:
            async with self._session.begin() as session:
                for_remove = await session.get(model, ident)
                await session.delete(for_remove)
        except UnmappedInstanceError:
            print(ident)

    async def update(self, model, identy, **kwargs):
        async with self._session.begin() as session:
            for_update = await session.get(model, identy)
            if for_update:
                for atr, val in kwargs.items():
                    for_update.__setattr__(atr, val)

    async def read(self, model, **kwargs):
        async with self._session.begin() as session:
            tup = model(**kwargs)
            query = select(model)
            for atr, val in kwargs.items():
                query = query.where(str(tup.__getattribute__(atr)) == str(val))
                print(query)
            results = (await session.execute(query)).scalars().all()
            return [str(i) for i in results]

    async def close_and_dispose(self):
        await self._engine.dispose()


if __name__ == "__main__":
    from db.models import Base
    import asyncio