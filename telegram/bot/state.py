from aiogram.filters.state import State, StatesGroup


class UserPhoneForm(StatesGroup):
    phone = State()


class ReplaceUserPhoneForm(StatesGroup):
    phone = State()
