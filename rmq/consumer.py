from rmq.connection import RMQConnection
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)

from typing import Any


class RMQConsumer(RMQConnection):
    @classmethod
    async def consume(cls, callback: callable) -> None:
        queue = await cls.create_queue()
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logger.info(message)
                    await callback(message)


rmq_consumer = RMQConsumer()
