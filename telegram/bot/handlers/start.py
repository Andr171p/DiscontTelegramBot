from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from telegram.bot.messages import IMessage
from telegram.bot.keyboards.register_kb import start_keyboard
from telegram.bot.keyboards.order_status_kb import order_status_keyboard

from api.registration.reg_service import registration_api

from rmq.consumer import rmq_consumer


start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    user_exists = await registration_api.check_user(user_id=user_id)
    if user_exists:
        await message.answer(
            IMessage.ALREADY_REGISTER_MESSAGE,
            reply_markup=await order_status_keyboard()
        )
    else:
        await message.answer(
            IMessage.start(username=username),
            reply_markup=await start_keyboard()
        )
    # await rmq_consumer.consume()
