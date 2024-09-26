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
            logger.info(RMQLoggingMessage.START_CONSUMING)
            await queue.consume(callback)


rmq_consumer = RMQConsumer()
