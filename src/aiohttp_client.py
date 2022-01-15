#import aiohttp
from aiohttp import ClientSession

aiohttp_session = None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class ClientIOHTTP(metaclass=Singleton):
    session: ClientSession = None
