from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    first_name = State()
    age = State()
    phone_number = State()
