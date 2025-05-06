from .external import MyExternalApiForBot
from aiohttp import ClientSession

__all__ = ["get_external_api_session_manager", "MyExternalApiForBot"]

external_api_session = None
external_api_manager = None

async def get_external_api_session_manager(rout: str = '') -> MyExternalApiForBot:
    global external_api_session, external_api_manager
    if external_api_session is None:
        external_api_session = ClientSession()
    external_api_manager = MyExternalApiForBot(r'http://127.0.0.1:8000/'+rout, external_api_session)
    return external_api_manager
