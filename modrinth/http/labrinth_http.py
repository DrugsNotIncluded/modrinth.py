import asyncio
from .abc import HTTPClient, DEFAULT_RATELIMIT, DEFAULT_RATELIMIT_INTERVAL, PROD_BASE_API, TEST_BASE_API
from .aiohttp_client import AiohttpClient
from ..types import GET, POST, DOWNLOAD, PUT, DEL, PATCH, endpoint
from typing import Optional
from urllib.parse import urlencode, quote_plus
from typing import Any

# There will be OAuth2 Authorization implementation:
# TODO

#  add response errors handler

DEFAULT_USERAGENT = "github.com/DrugsNotIncluded/modrinth.py (coffeemeowgirl@gmail.com , t.me/humanised_doll)"

class LabrinthHTTP:
    """
    Base Labrinth API class
    All ratelimit handling processed in AiohttpClient for now, i will add default implementation to HTTPClient class later.
    You have to provide UserAgent with contact info in it, otherwise Labrinth API will eventually stop working for your current IP.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        ratelimit: Optional[int] = None,
        ratelimit_interval: Optional[int] = None,
        user_agent: str = DEFAULT_USERAGENT,
        http_client: HTTPClient = AiohttpClient,
        _testing: Optional[bool] = False,
        _headers: Optional[dict] = None
        ):
        self._http_client = http_client(
            user_agent = DEFAULT_USERAGENT,
            api_key = api_key,
            testing = _testing,
            ratelimit = DEFAULT_RATELIMIT,
            ratelimit_interval = DEFAULT_RATELIMIT_INTERVAL)

    async def close(self):
        await self._http_client.close()

    async def get(self, endpoint: str, json: Optional[Any], _headers = Optional[dict]):
        return await self._http_client.get(endpoint, json=json, _headers=_headers)
    
    async def post(self, endpoint: str, data: dict, json: Optional[Any], _headers = Optional[dict]):
        return await self._http_client.post(endpoint, data=data, json=json, _headers=_headers)
    
    async def download(self, endpoint: str, chunk_size: int, json: Optional[Any], _headers = Optional[dict]):
        return await self._http_client.download(endpoint, chunk_size=chunk_size, json=json, _headers=_headers)

    async def put(self, endpoint: str, data: dict, json: Optional[Any], _headers = Optional[dict]):
        return await self._http_client.put(endpoint, data=data, json=json, _headers=_headers)

    async def delete(self, endpoint: str, json: Optional[Any], _headers = Optional[dict]):
        return await self._http_client.delete(endpoint, json=json, _headers=_headers)

    async def patch(self, endpoint: str, data: dict, json: Optional[Any], _headers = Optional[dict]):
        return await self._http_client.patch(endpoint, data=data, json=json, _headers=_headers)

    async def api(
        self,
        endpoint: endpoint,
        data: Optional[object] = None,
        params: Optional[dict] = None,
        query: Optional[dict] = None,
        chunk_size: Optional[int] = None,
        headers: Optional[dict] = None,
        json: Optional[Any] = None
        ):
        method = endpoint.method
        endpoint = endpoint.endpoint
        if params:
            endpoint = endpoint.format(**params)
        if query:
            query = urlencode(query)
            endpoint = endpoint + query
        if method == GET:
            return(await self.get(endpoint, json=json, _headers=headers))
        if method == POST:
            return(await self.post(endpoint, data=data, json=json, _headers=headers))
        if method == DOWNLOAD:
            return(await self.download(endpoint, json=json, chunk_size=chunk_size, _headers=headers))
        if method == PUT:
            return(await self.put(endpoint, data=data, json=json, _headers=headers))
        if method == DEL:
            return(await self.delete(endpoint, json=json, _headers=headers))
        if method == PATCH:
            return(await self.patch(endpoint, data=data, json=json, _headers=headers))