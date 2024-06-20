from aiogram.filters.state import State, StatesGroup


class UserPhoneNumberForm(StatesGroup):
    phone_number = State()
