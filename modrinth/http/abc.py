from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator
from typing import Any, Optional
import aiohttp
from aiohttp.client import DEFAULT_TIMEOUT, ClientTimeout

"""
There's standart ratelimit on modrinth, for now you must implement your own ratelimiting logic if you want to add new http client
You can look at default implementation in aiohttp_client.py, i will restructure code in the future to include this logic in abstract class
"""
DEFAULT_RATELIMIT = 300 
DEFAULT_RATELIMIT_INTERVAL = 60 # In seconds

TEST_BASE_API = 'https://staging-api.modrinth.com'
PROD_BASE_API = 'https://api.modrinth.com'

class HTTPClient(metaclass=ABCMeta):
    """required types"""

    def __init__(
        self,
        base_url: str,
        user_agent: str,
        testing: Optional[bool] = False,
        ratelimit: Optional[int] = DEFAULT_RATELIMIT,
        ratelimit_interval: Optional[int] = DEFAULT_RATELIMIT_INTERVAL,
        api_key: Optional[str] = None
        ) -> None:
        ...

    @property
    def headers(self):
        ...

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def get(self, url: str):
        ...

    @abstractmethod
    async def post(self, url: str, data: Optional[dict] = None):
        ...

    @abstractmethod
    async def download(self, url: str, chunk_size: int) -> AsyncIterator[bytes]:
        ...

    @abstractmethod
    async def put(self, url: str, data: Optional[dict] = None):
        ...

    @abstractmethod
    async def delete(self, url: str):
        ...

    @abstractmethod
    async def patch(self, url: str, data: Optional[dict] = None):
        ...