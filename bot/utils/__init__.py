from .external import MyExternalApiForBot
from aiohttp import ClientSession

__all__ = ['get_session_manager']

session = None
manager = None

async def get_session_manager():
    global session, manager
    session = ClientSession()
    manager = MyExternalApiForBot(r'http://127.0.0.1:8000/user', session)
    return manager
