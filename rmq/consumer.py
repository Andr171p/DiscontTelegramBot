from rmq.connection import RMQConnection
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)

from typing import Any


class RMQConsumer(RMQConnection):

    @classmethod
    async def consume(cls, queue: Any, callback: callable) -> None:
        '''await cls.connect()
        async with cls.connection:
            queue = await cls.create_queue()
            logger.info(RMQLoggingMessage.START_CONSUMING)
            await queue.consume(callback)
            await cls.close()'''
        async with queue.iterator() as queue:
            async for message in queue:
                await callback(message)

    @classmethod
    async def receive(cls) -> Any:
        await cls.connect()
        queue = await cls.create_queue()
        return queue


rmq_consumer = RMQConsumer()
