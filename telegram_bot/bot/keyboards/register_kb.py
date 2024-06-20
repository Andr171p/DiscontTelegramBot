from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from telegram_bot.bot.keyboards.buttons import RegisterButtons


async def start_keyboard():
    keyboard_list = [
        [KeyboardButton(
            text=RegisterButtons.start_register_button,
            request_contact=True
        )]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите для регистрации"
    )
    return keyboard
