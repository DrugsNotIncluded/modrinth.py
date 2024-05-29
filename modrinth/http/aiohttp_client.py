from abc import ABCMeta, abstractmethod
from .abc import HTTPClient
from collections.abc import AsyncIterator
from typing import Any, Optional
import aiohttp
from aiohttp.client import DEFAULT_TIMEOUT, ClientTimeout
from aiolimiter import AsyncLimiter
from .errors import DeprecatedAPI, InvalidScope
import asyncio

# Default Labrinth API ratelimits
DEFAULT_RATELIMIT = 300 
DEFAULT_RATELIMIT_INTERVAL = 60 # In seconds

TEST_BASE_API = 'https://staging-api.modrinth.com'
PROD_BASE_API = 'https://api.modrinth.com'   

# Dirty http client implementation with throttling support via aiolimiter
# In ideal world client shouldn't call asyncio.sleep at all

class AiohttpClient(HTTPClient):
    """An aiohttp impl for HTTPClient"""
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
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": user_agent
        }
        if api_key:
            _headers['Authorization'] = api_key
        if not testing:
            self._base_url = base_url
        else:
            self._base_url = TEST_BASE_API
        self._sess = aiohttp.ClientSession(
            base_url=self._base_url,
            headers=_headers,
            timeout=timeout,
            trust_env=True,
            raise_for_status=True
        )
        self._sess.trace_configs

    @property
    def headers(self):
        return self._sess.headers

    async def close(self):
        await self._sess.close()

    async def get(self, url: str):
        async with self.ratelimit:
            res = await self._sess.get(url)
        if res.status == 410:
            raise DeprecatedAPI
        if res.status == 401:
            raise InvalidScope
        if res.headers['X-Ratelimit-Remaining'] == 0:
            await asyncio.sleep(res.headers['X-Ratelimit-Reset'])
        return await res.json()

    async def post(self, url: str, data: Optional[dict] = None):
        async with self.ratelimit:
            res = await self._sess.post(url, data=data)
        if res.status == 410:
            raise DeprecatedAPI
        if res.status == 401:
            raise InvalidScope
        if res.headers['X-Ratelimit-Remaining'] == 0:
            await asyncio.sleep(res.headers['X-Ratelimit-Reset'])
        return await res.json()

    async def download(self, url: str, chunk_size: int) -> AsyncIterator[bytes]:
        async with self.ratelimit:
            res = await self._sess.get(url, allow_redirects=True)
        if res.status == 410:
            raise DeprecatedAPI
        if res.status == 401:
            raise InvalidScope
        if res.headers['X-Ratelimit-Remaining'] == 0:
            await asyncio.sleep(res.headers['X-Ratelimit-Reset'])
        return res.content.iter_chunked(chunk_size)

    @property
    def session(self):
        return self._sess