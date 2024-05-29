from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator
from typing import Any, Optional
import aiohttp
from aiohttp.client import DEFAULT_TIMEOUT, ClientTimeout

class HTTPClient(metaclass=ABCMeta):
    """required types"""

    def __init__(self, base_url: str, user_agent: str) -> None:
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