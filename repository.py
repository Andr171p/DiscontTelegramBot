from backend.client.order_status import OrdersAtTheMoment
from backend.client.order_status import PrettyStatus
from backend.client.order_status import TriggerOrdersStatus

from backend.database.auth_db.db_auth_manage import SuchefAuthDB
from backend.database.orders_db.db_orders_manage import OrdersEngineDB

from telegram.bot.keyboards.order_status_kb import pay_link_keyboard
from telegram.bot.keyboards.register_kb import re_register_keyboard

from telegram.bot.messages import MessageInterface

import asyncio


class OrdersRepository:
    def __init__(self):
        self.orders_at_the_moment = OrdersAtTheMoment()
        self.orders_engine_db = OrdersEngineDB()
        self.auth_engine_db = SuchefAuthDB()
        self.triggers = TriggerOrdersStatus.trigger_order_status

    async def order_status(self, user_id, message):
        phone_number = self.auth_engine_db.db_phone_number_from_id(telegram_id=user_id)
        orders = self.orders_engine_db.db_order_data_from_phone_number(
            phone_number=phone_number
        )
        if bool(orders):
            for order in orders:
                order_status = PrettyStatus(order=order).message()
                await message.answer(
                    order_status,
                    reply_markup=await pay_link_keyboard(pay_link=order['pay_link'])
                )
        else:
            await message.answer(MessageInterface().empty_order_message)
            await message.answer(MessageInterface().problem_status_message)
            await message.answer(
                MessageInterface(user_phone_number=phone_number).phone_number_question(),
                reply_markup=await re_register_keyboard()
            )

    async def check_trigger_status(self, user_id, message, timeout=60):
        while True:
            phone_number = self.auth_engine_db.db_phone_number_from_id(
                telegram_id=user_id
            )
            orders = self.orders_engine_db.db_check_trigger_status(
                phone_number=phone_number,
                triggers=self.triggers
            )
            print(orders)
            if bool(orders):
                for order in orders:
                    print(order)
                    sent = self.orders_engine_db.db_check_sent(phone_number=phone_number)
                    print(sent)
                    if not sent:
                        status = PrettyStatus(order=order).message()
                        await message.answer(
                            status,
                            reply_markup=await pay_link_keyboard(pay_link=order['pay_link'])
                        )
                        self.orders_engine_db.db_update_sent(
                            phone_number=phone_number,
                            triggers=self.triggers
                        )
            await asyncio.sleep(timeout)
