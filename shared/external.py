import logging
from functools import wraps

from aiohttp import ClientResponseError, ClientSession
from aiohttp.client_exceptions import ClientConnectorError

log = logging.getLogger(__name__)


def handle_ext_api(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except ClientConnectorError:
            log.warning("поключение не установлено")

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
        try:
            url = self._url + prefix
            async with self._session.post(url, json=data) as res:
                log.info("res: %s", res)
                res.raise_for_status()
                return await res.json()
        except ClientResponseError:
            return None

    async def remove(self, prefix: str, **args):
        try:
            async with self._session.delete(self._url + prefix, params=args) as res:
                res.raise_for_status()
                return await res.json()
        except ClientResponseError:
            return None

    async def read(self, prefix: str, **kwargs):
        try:
            async with self._session.get(self._url + prefix, params=kwargs) as res:
                res.raise_for_status()
                return await res.json()
        except ClientResponseError:
            return None

    async def update(self, prefix: str, **kwargs):
        try:
            async with self._session.patch(self._url + prefix, json=kwargs) as res:
                res.raise_for_status()
                return await res.json()
        except ClientResponseError:
            return None

    async def connect(self):
        log.info("connect to external")
        if not self._session:
            self._session = ClientSession()
            log.debug("сессия создана")

    async def close(self):
        if self._session:
            log.warning(f"закрываю сессию {self.__class__.__name__}")
            await self._session.close()
            self._session = None
