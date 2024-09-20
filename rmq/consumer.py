from rmq.connect import RMQConnection
from rmq.settings.queue_config import QueueConfig
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)


class RMQConsumeMessage(RMQConnection):
    @staticmethod
    def callback(ch, method, properties, body) -> None:
        logger.info(f"[x] Received {body}")

    async def consume(self) -> None:
        logger.info(RMQLoggingMessage.START_CONSUMING)
        self.channel.basic_consume(
            queue=QueueConfig.QUEUE_NAME,
            on_message_callback=self.callback,
            auto_ack=True
        )
        self.channel.start_consuming()


rmq_consumer = RMQConsumeMessage()
