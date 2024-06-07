from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator
from typing import Any, Optional, Callable
import aiohttp
from aiohttp.client import DEFAULT_TIMEOUT, ClientTimeout
from aiolimiter import AsyncLimiter
from .errors import *


class HTTPClient(metaclass=ABCMeta):
    """
    Base HTTP client class with inbuild ratelimiter
    All requests functions with 'json' argument must have a way to automatically add appropriate headers (as in aiohttp.post, for example) and serialize input or you must manually implement it
    All requests functions must return status as first parameter
    """
    def __init__(self,
        user_agent: str,
        testing: Optional[bool] = False,
        ratelimit: Optional[int] = 300, 
        ratelimit_interval: Optional[int] = 60,
        api_key: Optional[str] = None
        ) -> None:

        TEST_BASE_API = 'https://staging-api.modrinth.com'
        PROD_BASE_API = 'https://api.modrinth.com'
        self.headers = {"User-Agent": user_agent}
        if api_key: self.headers['Authorization'] = api_key
        self.base_url = PROD_BASE_API if not testing else TEST_BASE_API
        self.ratelimit = ratelimit
        self.ratelimit_interval = ratelimit_interval
        self.ratelimiter = AsyncLimiter(self.ratelimit, self.ratelimit_interval)

    @property
    @abstractmethod
    def session(self):
        """Returns http client session (aiohttp, httpx or whatever you use)"""
        ...

    @abstractmethod
    async def close(self):
        """Closes all connections for current session"""
        ...

    @StatusResolver
    @abstractmethod
    async def get(self, url: str) -> tuple[int, Optional[Any]]:
        ...

    @StatusResolver
    @abstractmethod
    async def post(self, url: str, data: Optional[dict] = None, json: Optional[Any] = None) -> tuple[int, Optional[Any]]:
        ...

    @StatusResolver
    @abstractmethod
    async def download(self, url: str, chunk_size: int, json: Optional[Any] = None) -> tuple[int, AsyncIterator[bytes]]:
        ...

    @StatusResolver
    @abstractmethod
    async def put(self, url: str, data: Optional[dict] = None, json: Optional[Any] = None) -> tuple[int, Optional[Any]]:
        ...

    @StatusResolver
    @abstractmethod
    async def delete(self, url: str) -> tuple[int, Optional[Any]]:
        ...

    @StatusResolver
    @abstractmethod
    async def patch(self, url: str, data: Optional[dict] = None, json: Optional[Any] = None) -> tuple[int, Optional[Any]]:
        ...