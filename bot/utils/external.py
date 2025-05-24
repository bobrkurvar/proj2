from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from core import logger


class MyExternalApiForBot:
    def __init__(self, url, session: ClientSession):
        self._url = url
        self._session = session

    async def create(self, prefix: str, **data):
        try:
            todo_id = None
            async with self._session.post(self._url+ prefix + '/create', json = data) as response:
                todo_id = response
            return todo_id
        except ClientConnectorError:
            return None

    async def remove(self, prefix: str, **args):
        try:
            await self._session.get(self._url + prefix + '/delete', params=args)
        except ClientConnectorError:
            return None

    async def read(self, prefix: str, **indent):
        try:
            res = await self._session.get(self._url + prefix + '/read', params=indent)
            res = await res.json()
        except ClientConnectorError:
            return None
        return res

    async def update(self, prefix: str, **kwargs):
        try:
            await self._session.patch(self._url + prefix + '/update', json=kwargs)
        except ClientConnectorError:
            pass

    async def close(self):
        if self._session is not None:
            logger.info(f'закрываю сессию {self.__class__.__name__}')
            await self._session.close()
            self._session = None

