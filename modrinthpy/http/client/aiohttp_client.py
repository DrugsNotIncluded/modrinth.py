from abc import ABCMeta, abstractmethod
from ..abc import HTTPClient
from collections.abc import AsyncIterator
from typing import Any, Optional
import aiohttp
from aiohttp.client import DEFAULT_TIMEOUT, ClientTimeout
from aiolimiter import AsyncLimiter
from ..errors import *
import asyncio

class AiohttpClient(HTTPClient):
    """
    Default aiohttp based HTTP client implementation
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sess = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(force_close=True, enable_cleanup_closed=True),
            base_url=self.base_url,
            headers=self.headers,
            timeout=DEFAULT_TIMEOUT,
            trust_env=True,
        )

    @property
    def session(self):
        return self._sess

    async def close(self):
        await self._sess.close()

    @StatusResolver
    async def get(self, url: str) -> tuple[int, Optional[Any]]:
        async with self.ratelimiter:
            result = await self._sess.get(url, headers = self.headers)
        return result.status, result.content

    @StatusResolver
    async def post(self, url: str, data: Optional[dict] = None, json: Optional[Any] = None) -> tuple[int, Optional[Any]]:
        async with self.ratelimiter:
            result = await self._sess.post(url, headers = self.headers , data=data, json=json)
        return result.status, result.content

    @StatusResolver
    async def download(self, url: str, chunk_size: int, json: Optional[Any] = None) -> tuple[int, AsyncIterator[bytes]]:
        async with self.ratelimiter:
            result = await self._sess.get(url, allow_redirects=True, headers=headers, json=json)
        return result.status, result.content.iter_chunked

    @StatusResolver
    async def put(self, url: str, data: Optional[dict] = None, json: Optional[Any] = None) -> tuple[int, Optional[Any]]:
        async with self.ratelimiter:
            result = await self._sess.put(url, data=data, headers=self.headers)
        return result.status, result.content

    @StatusResolver
    async def delete(self, url: str) -> tuple[int, Optional[Any]]:
        async with self.ratelimiter:
            result = await self._sess.delete(url, headers=self.headers)
        return result.status, result.content

    @StatusResolver
    async def patch(self, url: str, data: Optional[dict] = None, json: Optional[Any] = None) -> tuple[int, Optional[Any]]:
        async with self.ratelimiter:
            result = await self._sess.patch(url, data=data, headers=self.headers, json=json)
        return result.status, result.content