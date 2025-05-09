from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError


class MyExternalApiForBot:
    def __init__(self, url, session: ClientSession):
        self._url = url
        self._session = session

    async def create(self, prefix: str, **data):
        try:
            await self._session.post(self._url+ prefix + '/create', json = data)
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

    async def close(self):
        if self._session is not None:
            print(f'закрываю сессию {self.__class__.__name__}')
            await self._session.close()
            self._session = None
