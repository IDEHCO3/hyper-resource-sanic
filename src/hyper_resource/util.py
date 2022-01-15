import re
import aiohttp
import httpx

from src.hyper_resource.common_resource import CONTENT_TYPE_WKB, CONTENT_TYPE_JSON


def convert_camel_case_to_hifen(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def convert_camel_case_to_underline(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

async def a_request(url: str, accept: str = CONTENT_TYPE_JSON):
    #aiohttp_session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    headers = {'accept': accept}
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp


async def get_request(url, accept: str = CONTENT_TYPE_JSON):
    async with httpx.AsyncClient() as client:
        headers = {'accept': accept}
        return await client.get(url, headers=headers)

def value_has_url(value_str: str) -> bool:
    return (value_str.find('http:') > -1) or (value_str.find('https:') > -1) or (value_str.find('www.') > -1)