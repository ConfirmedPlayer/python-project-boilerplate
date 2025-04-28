import orjson
from aiohttp import ClientResponse, ClientSession

from tools import ABCSingleton
from tools.http import ABCHTTPClient


class AiohttpClient(ABCHTTPClient):
    def __init__(self) -> None:
        self.json_processing_module = orjson

    async def request_raw(
        self, url: str, method: str = 'GET', data: dict | None = None, **kwargs
    ) -> ClientResponse:
        if not self.session:
            self.session = ClientSession(
                json_serialize=self.json_processing_module.dumps,
                **self._session_params,
            )
        async with self.session.request(
            url=url, method=method, data=data, **kwargs
        ) as response:
            await response.read()
            return response

    async def request_json(
        self, url: str, method: str = 'GET', data: dict | None = None, **kwargs
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding='UTF-8',
            loads=self.json_processing_module.loads,
            content_type=None,
        )

    async def request_text(
        self, url: str, method: str = 'GET', data: dict | None = None, **kwargs
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding='UTF-8')

    async def request_content(
        self, url: str, method: str = 'GET', data: dict | None = None, **kwargs
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        assert response._body is not None
        return response._body

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def __del__(self) -> None:
        if self.session and not self.session.closed:
            if (
                self.session._connector is not None
                and self.session._connector_owner
            ):
                self.session._connector._close()
            self.session._connector = None


class SingleAiohttpClient(AiohttpClient, ABCSingleton):
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass
