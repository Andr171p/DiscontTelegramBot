from rmq.connect import RMQConnection
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)


class RMQConsumer(RMQConnection):

    @classmethod
    async def consume(cls, callback: callable) -> None:
        await cls.connect()
        async with cls.connection:
            queue = await cls.create_queue()
            await queue.consume(callback)
            logger.info(RMQLoggingMessage.START_CONSUMING)


rmq_consumer = RMQConsumer()
