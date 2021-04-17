import asyncio
import re

import aiohttp


def convert_camel_case_to_hifen(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def convert_camel_case_to_underline(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

async def get_session_request(url: str):
    #aiohttp_session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    aiohttp_session = aiohttp.ClientSession()
    response = await aiohttp_session.get(url)
    await aiohttp_session.close()
    return response
