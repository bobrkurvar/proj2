from aiohttp import ClientSession

class MyExternalApiForBot:
    def __init__(self, url, session: ClientSession):
        self._url = url
        self._session = session

    async def register_for_bot(self, **data):
        await self._session.post(self._url+'/start-register', json = data)

    async def remove_from_bot(self, **args):
        await self._session.get(self._url+'/remove-from-bot', params=args)

    async def close(self):
        await self._session.close()


