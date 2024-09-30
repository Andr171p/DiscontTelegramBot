from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram.bot.storage import user_info_storage
from telegram.bot.messages import IMessage
from telegram.bot.keyboards.register_kb import check_phone_number_keyboard
from telegram.bot.keyboards.order_status_kb import order_status_keyboard
from telegram.bot.keyboards.buttons import RegisterCallBacks
from telegram.bot.state import (
    UserPhoneForm,
    ReplaceUserPhoneForm
)

from api.registration.reg_service import registration_api

from misc.format import format_phone

from loguru import logger


register_router = Router()


@register_router.message(F.contact)
async def register_user_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    phone = format_phone(message.contact.phone_number)

    user_info_storage.add(
        user_id=user_id,
        username=username,
        phone=phone
    )
    logger.info(f"START REGISTER USER: {user_info_storage}")
    await message.answer(
        IMessage.phone_question(phone=phone),
        reply_markup=await check_phone_number_keyboard()
    )


@register_router.callback_query(F.data == RegisterCallBacks.valid_phone_callback)
async def valid_phone_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    data = user_info_storage.data()
    user_id, username, phone = data['user_id'], data['username'], data['phone']
    _user = await registration_api.create_user(
        user_id=user_id,
        username=username,
        phone=phone
    )
    logger.info(f"USER CREATED: {user_info_storage}")
    await callback.message.answer(
            IMessage.SUCCESS_REGISTER_MESSAGE,
            reply_markup=await order_status_keyboard()
    )


@register_router.callback_query(F.data == RegisterCallBacks.invalid_phone_callback)
async def invalid_phone_handler(
        callback: CallbackQuery, state: FSMContext
) -> None:
    await callback.answer()
    await state.set_state(UserPhoneForm.phone)
    await callback.message.answer(IMessage.INPUT_PHONE_NUMBER_MESSAGE)


@register_router.message(UserPhoneForm.phone)
async def input_phone_handler(
        message: Message, state: FSMContext
) -> None:
    phone = message.text
    await state.update_data(phone=phone)
    logger.info(f"USER WRITE PHONE NUMBER: {phone}")
    data = await state.get_data()
    user_info = user_info_storage.data()
    user_id, username, phone = user_info['user_id'], user_info['username'], format_phone(data['phone'])
    _user = await registration_api.create_user(
        user_id=user_id,
        username=username,
        phone=phone
    )
    user_info_storage.clear()
    await message.answer(
        IMessage.SUCCESS_REGISTER_MESSAGE,
        reply_markup=await order_status_keyboard()
    )
    await state.clear()


@register_router.callback_query(F.data == RegisterCallBacks.correct_phone_callback)
async def correct_phone_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(IMessage.WAIT_STATUS_MESSAGE)


@register_router.callback_query(F.data == RegisterCallBacks.incorrect_phone_callback)
async def incorrect_phone_handler(
        callback: CallbackQuery, state: FSMContext
) -> None:
    await callback.answer()
    await state.set_state(ReplaceUserPhoneForm.phone)
    await callback.message.answer(
        IMessage.INPUT_PHONE_NUMBER_MESSAGE
    )


@register_router.message(ReplaceUserPhoneForm.phone)
async def replace_phone_handler(
        message: Message, state: FSMContext
) -> None:
    user_id = message.from_user.id
    phone = message.text
    logger.info(f"USER WRITE PHONE: {phone}")
    await state.update_data(phone=phone)
    data = await state.get_data()
    phone = format_phone(phone=data['phone'])
    user = await registration_api.replace_phone(
        user_id=user_id,
        phone=phone
    )
    logger.info(user)
    await message.answer(
        IMessage.SUCCESS_REGISTER_MESSAGE,
        reply_markup=await order_status_keyboard()
    )
    await state.clear()
