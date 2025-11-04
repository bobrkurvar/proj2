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
    api_methods = {"create", "remove", "read", "update"}
    for name in api_methods:
        if hasattr(cls, name):
            method = getattr(cls, name)
            setattr(cls, name, handle_ext_api(method))
    return cls

@add_exception_handler
class MyExternalApiForBot:
    def __init__(self, url):
        self._url = url
        self._session = None


    async def create(self, prefix: str, **data):
        async with self._session.post(self._url+ prefix, json = data) as res:
            return await res.json()

    async def remove(self, prefix: str, **args):
        async with self._session.delete(self._url + prefix, params=args) as res:
            return await res.json()

    async def read(self, prefix: str, **kwargs):
        async with self._session.get(self._url + prefix, params=kwargs) as res:
            return await res.json()

    async def update(self, prefix: str, **kwargs):
        async with self._session.patch(self._url + prefix, json=kwargs) as res:
            return await res.json()

    async def connect(self):
        if not self._session:
            self._session = ClientSession()

    async def close(self):
        if self._session:
            log.warning(f'закрываю сессию {self.__class__.__name__}')
            await self._session.close()
            self._session = None

