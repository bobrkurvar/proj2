from .external import MyExternalApiForBot
from aiohttp import ClientSession


external_api_manager = MyExternalApiForBot(r'http://127.0.0.1:8000/')
session = None

async def init_external_api_session():
    global session, external_api_manager
    session = ClientSession()
    await external_api_manager.begin(session)

async def close_external_api_manager():
    await external_api_manager.close()


