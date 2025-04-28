from abc import ABC, abstractmethod
from typing import Any


class ABCHTTPClient(ABC):
    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    async def request_raw(
        self,
        url: str,
        method: str = 'GET',
        data: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = 'GET',
        data: dict | None = None,
        **kwargs: Any,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = 'GET',
        data: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = 'GET',
        data: dict | None = None,
        **kwargs: Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> 'ABCHTTPClient':
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()
