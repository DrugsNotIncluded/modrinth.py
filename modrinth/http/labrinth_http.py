import asyncio
from .abc import HTTPClient
from .aiohttp_client import AiohttpClient
from ..types import GET, POST, DOWNLOAD, endpoint
from typing import Optional

# There will be OAuth2 Authorization implementation:
# TODO

class LabrinthHTTP:
    """
    Base Labrinth API class
    All ratelimit handling processed in AiohttpClient for now, i will add default implementation to HTTPClient class later.
    You have to provide UserAgent with contact info in it, otherwise Labrinth API will eventually stop working for your current IP.
    """
    def __init__(
        user_agent: str,
        http_client: HTTPClient = AiohttpClient,
        api_key: Optional[str] = None,
        **http_client_args
        ):
        args = {"user_agent":user_agent, "api_key":api_key}.update(**http_client_args)
        self._http_client = http_client(**args)

    async def close(self):
        await self._http_client.close()

    async def get(self, endpoint: str):
        return await self._http_client.get(endpoint)
    
    async def post(self, endpoint: str, data: dict):
        return await self._http_client.post(endpoint, data=data)
    
    async def download(self, endpoint: str, chunk_size: int):
        return await self._http_client.download(endpoint, chunk_size=chunk_size)

    async def api(
        self,
        endpoint: endpoint,
        data: Optional[object] = None,
        params: Optional[dict] = None,
        query: Optional[dict] = None,
        chunk_size: Optional[int] = None
        ):
        method = endpoint.method
        endpoint = endpoint.endpoint
        if query:
            query = urlencode(query)
        if params:
            endpoint = endpoint.format(**params)
        endpoint = endpoint + query
        if method == GET:
            return(await self.get(endpoint))
        if method == POST:
            return(await self.post(endpoint, data))
        if method == DOWNLOAD:
            return(await self.download(endpoint, chunk_size))