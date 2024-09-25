import aio_pika

from rmq.settings.server_config import ConnectData
from rmq.settings.queue_config import QueueConfig
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)

from typing import Any


class RMQConnection:
    connection = None
    channel = None

    @classmethod
    async def connect(cls) -> None:
        cls.connection = await aio_pika.connect_robust(ConnectData.RMQ_URL)
        cls.channel = await cls.connection.channel()
        logger.info(RMQLoggingMessage.SUCCESSFUL_CONNECT)

    @classmethod
    async def create_queue(cls) -> Any:
        if cls.channel is None:
            await cls.connect()
        queue = await cls.channel.declare_queue(QueueConfig.QUEUE_NAME)
        return queue

    @classmethod
    async def close(cls) -> None:
        await cls.connection.close()
