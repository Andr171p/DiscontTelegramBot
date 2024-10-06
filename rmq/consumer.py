from rmq.connection import RMQConnection
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)

from typing import Any


class RMQConsumer(RMQConnection):

    @classmethod
    async def consume(cls, queue: Any, callback: callable) -> None:
        logger.info(RMQLoggingMessage.START_CONSUMING)
        async with queue.iterator() as queue:
            async for message in queue:
                logger.info(message)
                await callback(message)

    @classmethod
    async def receive(cls) -> Any:
        await cls.connect()
        queue = await cls.create_queue()
        await cls.close()
        return queue


rmq_consumer = RMQConsumer()
