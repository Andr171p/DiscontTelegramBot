import aiohttp
from aiohttp import ClientResponse

from api.logs import logger
from api.logs import RequestLoggingMessage
from api.config import HTTPConfig


class HTTPSession:
    requestData = HTTPConfig()

    @staticmethod
    def is_ok(response: ClientResponse) -> bool:
        status = response.status
        return True if status in range(200, 300) else False

    @classmethod
    async def get_request(cls, url: str) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url,
                    headers=cls.requestData.HEADERS,
                    timeout=cls.requestData.TIMEOUT
                ) as response:
                    if cls.is_ok(response=response):
                        result = await response.json()
                        logger.info(RequestLoggingMessage.successful_response)
                        logger.info(f"RESPONSE: {result}")
                        return result
        except Exception as _ex:
            logger.info(_ex)

    @classmethod
    async def post_request(cls, url: str, data: dict):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    headers=cls.requestData.HEADERS,
                    json=data,
                    timeout=cls.requestData.TIMEOUT
                ) as response:
                    if cls.is_ok(response=response):
                        result = await response.json()
                        logger.info(RequestLoggingMessage.successful_response)
                        logger.info(f"RESPONSE: {result}")
                        return result
        except Exception as _ex:
            logger.info(_ex)
