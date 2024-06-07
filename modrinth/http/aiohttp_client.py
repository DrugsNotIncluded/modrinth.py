from abc import ABCMeta, abstractmethod
from .abc import HTTPClient, DEFAULT_RATELIMIT, DEFAULT_RATELIMIT_INTERVAL, TEST_BASE_API, PROD_BASE_API
from collections.abc import AsyncIterator
from typing import Any, Optional
import aiohttp
from aiohttp.client import DEFAULT_TIMEOUT, ClientTimeout
from aiolimiter import AsyncLimiter
from .errors import *
import asyncio

# Dirty http client implementation with throttling support via aiolimiter
# In ideal world client shouldn't call asyncio.sleep at all

class AiohttpClient(HTTPClient):
    """An aiohttp impl for HTTPClient
    You don't have to close connections manually, but it's recommended."""
    def __init__(
        self,
        user_agent: str,
        api_key: Optional[str] = None,
        base_url: str = 'https://api.modrinth.com',
        testing: bool = False,
        ratelimit: int = DEFAULT_RATELIMIT,
        ratelimit_interval = DEFAULT_RATELIMIT_INTERVAL,
        timeout: ClientTimeout = DEFAULT_TIMEOUT
        ) -> None:

        self.max_ratelimit = ratelimit
        self.ratelimit_interval = ratelimit_interval
        self.ratelimit = AsyncLimiter(ratelimit, ratelimit_interval)
        self.ratelimit_headers = dict

        _headers = {
            "User-Agent": user_agent
        }
        if api_key:
            _headers['Authorization'] = api_key
        if not testing:
            self._base_url = base_url
        else:
            self._base_url = TEST_BASE_API
        self._sess = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(force_close=True, enable_cleanup_closed=True),
            base_url=self._base_url,
            headers=_headers,
            timeout=timeout,
            trust_env=True,
        )
        self._sess.trace_configs

    @staticmethod
    async def _resolve_http(response) -> None:
        if response.status == 204:
            return {'text':'OK'}
        if response.status == 410:
            raise DeprecatedAPI(response.text)
        if response.status == 401:
            raise InvalidScope(response.text)
        if response.status == 404:
            raise NotFound(response.text)
        if response.headers['X-Ratelimit-Remaining'] == 0:
            await asyncio.sleep(res.headers['X-Ratelimit-Reset'])

    @property
    def headers(self):
        """
        Global session headers modification, nonusable otherwise
        """
        return self._sess.headers

    async def close(self):
        await self._sess.close()

    async def get(self, url: str, json: Optional[Any], _headers = Optional[dict]):
        async with self.ratelimit:
            res = await self._sess.get(url, headers=_headers, json=json)
        h = await self._resolve_http(res)
        if h: return h
        return await res.json()

    async def post(self, url: str, data: Optional[dict], json: Optional[Any], _headers = Optional[dict]):
        async with self.ratelimit:
            res = await self._sess.post(url, data=data, headers=_headers, json=json)
        h = await self._resolve_http(res)
        if h: return h
        return await res.json()

    async def download(self, url: str, json: Optional[Any], chunk_size: int, _headers = Optional[dict]) -> AsyncIterator[bytes]:
        async with self.ratelimit:
            res = await self._sess.get(url, allow_redirects=True, headers=_headers, json=json)
        h = await self._resolve_http(res)
        if h: return h
        return res.content.iter_chunked(chunk_size)

    async def put(self, url: str, data: Optional[dict], json = Optional[Any], _headers = Optional[dict]):
        async with self.ratelimit:
            res = await self._sess.put(url, data=data, headers=_headers, json=json)
        h = await self._resolve_http(res)
        if h: return h
        return await res.json()

    async def delete(self, url: str, json = Optional[Any], _headers = Optional[dict]):
        async with self.ratelimit:
            res = await self._sess.delete(url, headers=_headers, json=json)
        await self._resolve_http(res)
        h = await self._resolve_http(res)
        if h: return h
        return res.json()

    async def patch(self, url: str, data: Optional[dict], json: Optional[Any], _headers = Optional[dict]):
        async with self.ratelimit:
            res = await self._sess.patch(url, data=data, headers=_headers, json=json)
        h = await self._resolve_http(res)
        if h: return h
        return await res.json()

    @property
    def session(self):
        return self._sess

# TODO: I DEFINITELY SHOULD rewrite error and response handling with decorators