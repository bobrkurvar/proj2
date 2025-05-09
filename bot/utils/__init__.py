from aiohttp import ClientSession
from .external import MyExternalApiForBot


async def get_ext_api_manager():
    session = ClientSession()
    return MyExternalApiForBot('http://127.0.0.1:8000/', session)










