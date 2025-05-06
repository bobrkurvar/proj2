from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

class MyExternalApiForBot:
    def __init__(self, url, session: ClientSession):
        self._url = url
        self._session = session

    async def create(self, **data):
        try:
            await self._session.post(self._url+'/create', json = data)
        except ClientConnectorError:
            return None

    async def remove(self, **args):
        try:
            await self._session.get(self._url + '/delete', params=args)
        except ClientConnectorError:
            return None

    async def read(self, **indent):
        try:
            res = await self._session.get(self._url + '/read', params=indent)
            res = await res.json()
        except ClientConnectorError:
            return None
        return res

    async def close(self):
        await self._session.close()


