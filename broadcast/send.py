from rmq.consumer import rmq_consumer
from rmq.settings.logs import (
    logger,
    RMQLoggingMessage
)

from broadcast.set_bot import SetBot
from broadcast.process import (
    check_status,
    Message
)

from telegram.bot.keyboards.order_status_kb import pay_link_keyboard

import asyncio
from aio_pika.abc import AbstractIncomingMessage


class Broadcast(SetBot):
    async def callback(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            logger.info(RMQLoggingMessage.START_PROCESS_MESSAGE)
            message_body = await Message(body=message.body).message()
            logger.info(RMQLoggingMessage.CONSUMED_MESSAGE.format(message=message))
            if check_status(message=message_body):
                await self.bot.send_message(
                    chat_id=message_body['user_id'],
                    text=message_body['message'],
                    reply_markup=await pay_link_keyboard(pay_link=message_body['pay_link'])
                )
                logger.info(RMQLoggingMessage.SUCCESSFUL_SEND_MESSAGE.format(message=message))
            await message.ack()

    async def broadcast(self, timeout: float = 60) -> None:
        while True:
            await rmq_consumer.consume(callback=self.callback)
            logger.info("STOP CONSUMING, WAITING 60s ...")
            await asyncio.sleep(timeout)
