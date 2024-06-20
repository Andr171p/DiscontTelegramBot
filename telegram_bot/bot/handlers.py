from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.bot.messages import MessageInterface

from telegram_bot.bot.keyboards.register_kb import start_keyboard, check_phone_number_keyboard
from telegram_bot.bot.keyboards.order_status_kb import order_status_keyboard, pay_link_keyboard
from telegram_bot.bot.keyboards.buttons import OrderStatusButtons
from telegram_bot.bot.state import UserPhoneNumberForm
from telegram_bot.bot.storage import UserInfoStorage

from backend.database.db_manage import SuchefAuthDB
from backend.client.order_status import ClientOrder

from misc.utils import format_phone_number

import time
import asyncio


router = Router()

suchef_auth_db = SuchefAuthDB()

user_info_storage = UserInfoStorage()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_name = message.from_user.first_name

    user_id = message.from_user.id

    if suchef_auth_db.db_check_user_id_exists(telegram_id=user_id):
        await message.answer(
            MessageInterface().already_register_message,
            reply_markup=await order_status_keyboard()
        )
    else:
        await message.answer(
            MessageInterface(user_name).start_message(),
            reply_markup=await start_keyboard()
        )


@router.message(F.contact)
async def insert_phone_number_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_phone = format_phone_number(message.contact.phone_number)

    user_info_storage.add(
        telegram_user_id=user_id,
        telegram_username=username,
        telegram_phone_number=user_phone
    )

    await message.answer(
        f"{MessageInterface().check_phone_number_message}{user_phone}",
        reply_markup=await check_phone_number_keyboard()
    )


@router.callback_query(F.data == 'valid_phone_number')
async def valid_phone_number_handler(callback: CallbackQuery):
    await callback.answer()

    user_info = user_info_storage.data()

    user_id = user_info[0]
    username = user_info[1]
    user_phone = user_info[2]

    suchef_auth_db.db_insert_user_auth_data(
        telegram_id=user_id,
        telegram_user=username,
        user_phone_number=user_phone
    )

    await callback.message.answer(
        MessageInterface().success_register_message,
        reply_markup=await order_status_keyboard()
    )


@router.callback_query(F.data == 'invalid_phone_number')
async def invalid_phone_number_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(UserPhoneNumberForm.phone_number)
    await callback.message.answer(
        MessageInterface().input_phone_number_message
    )


@router.message(UserPhoneNumberForm.phone_number)
async def input_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()

    user_info = user_info_storage.data()

    user_id = user_info[0]
    username = user_info[1]
    user_phone = format_phone_number(data["phone_number"])

    suchef_auth_db.db_insert_user_auth_data(
        telegram_id=user_id,
        telegram_user=username,
        user_phone_number=user_phone
    )

    await asyncio.sleep(3)

    await message.answer(
        MessageInterface().success_register_message,
        reply_markup=await order_status_keyboard()
    )


@router.message(F.text == OrderStatusButtons.get_status_button)
async def order_status_handler(message: Message):
    user_id = message.from_user.id

    phone_number = suchef_auth_db.db_phone_number_from_id(
        telegram_id=user_id
    )

    await message.answer(MessageInterface().search_order_message)

    client_order = ClientOrder(
        client_phone_number=phone_number
    )
    response = client_order.get_order_status()

    if response == -1 or len(response) == 0:
        await message.answer(MessageInterface().empty_order_message)
    else:
        for i in range(len(response)):
            time.sleep(1)
            if len(response[i]) != 1:
                await message.answer(
                    response[i][0],
                    reply_markup=await pay_link_keyboard(pay_link=response[i][-1])
                )
            else:
                await message.answer(
                    response[i][0]
                )
