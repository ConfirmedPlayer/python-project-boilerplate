import asyncio
from tools.http import SingleAiohttpClient
from core.logging import configure_logging


async def main():
    try:
        configure_logging()
    finally:
        await SingleAiohttpClient().close()


if __name__ == '__main__':
    asyncio.run(main())
