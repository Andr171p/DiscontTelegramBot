import pika

from rmq.settings.server_config import ConnectData
from rmq.settings.queue_config import QueueConfig
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)


class RMQConnection:
    connection = pika.BlockingConnection(
        pika.URLParameters(ConnectData.RMQ_URL)
    )
    channel = connection.channel()
    logger.info(RMQLoggingMessage.SUCCESSFUL_CONNECT)

    @classmethod
    def create_queue(cls) -> None:
        cls.channel.queue_declare(QueueConfig.QUEUE_NAME)

    @classmethod
    def close(cls) -> None:
        cls.connection.close()