from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
import logging
from functools import wraps

log = logging.getLogger(__name__)

def handle_ext_api(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except ClientConnectorError:
            log.warning('поключение не установлено')
    return wrapper

def add_exception_handler(cls):
    api_methods = ["create", "remove", "read", "update"]
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if attr in api_methods:
            setattr(cls, attr_name, handle_ext_api(attr))
    return cls

@add_exception_handler
class MyExternalApiForBot:
    _session = None
    def __init__(self, url):
        self._url = url
        if self.__class__._session is None:
            self._session = ClientSession()

    async def create(self, prefix: str, **data):
        res = await self._session.post(self._url+ prefix, json = data)
        return res

    async def remove(self, prefix: str, **args):
        await self._session.delete(self._url + prefix, params=args)

    async def read(self, prefix: str, **kwargs):
        res = await self._session.get(self._url + prefix, params=kwargs)
        res = await res.json()
        return res

    async def update(self, prefix: str, **kwargs):
        await self._session.patch(self._url + prefix, json=kwargs)

    # async def connect(self):
    #     if not self._session:
    #         self._session = ClientSession()

    async def close(self):
        if self._session:
            log.warning(f'закрываю сессию {self.__class__.__name__}')
            await self._session.close()
            self._session = None

