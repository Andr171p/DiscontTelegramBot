from aiogram import F, Router
from aiogram.types import Message

from telegram.bot.keyboards.buttons import OrderStatusButtons
from telegram.bot.keyboards.order_status_kb import pay_link_keyboard
from telegram.bot.keyboards.register_kb import re_register_keyboard
from telegram.bot.messages import IMessage

from api.status.status_service import status_api
# from api.registration.reg_service import registration_api

from cache.manager import cache_users_manager


status_router = Router()


@status_router.message(F.text == OrderStatusButtons.get_status_button)
async def order_status_handler(message: Message):
    user_id = message.from_user.id
    # phone = await registration_api.get_phone(user_id=user_id)
    phone = await cache_users_manager.get_cache_phone(user_id=user_id)
    orders = await status_api.user_orders(phone=phone)
    if len(orders) != 0:
        for order in orders:
            await message.answer(
                order['message'],
                reply_markup=await pay_link_keyboard(pay_link=order['pay_link'])
            )
    else:
        await message.answer(IMessage.EMPTY_ORDER_MESSAGE)
        await message.answer(IMessage.PROBLEM_STATUS_MESSAGE)
        await message.answer(
            IMessage.phone_question(phone=phone),
            reply_markup=await re_register_keyboard()
        )
