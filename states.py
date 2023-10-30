import re
from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    first_name = State()
    age = State()
    phone_number = State()


class Fedbik(StatesGroup):
    content = State()


def validate_phone_number(phone_number):
    pattern = r'^\+998\d{9}$|^\d{9}$'
    match = re.match(pattern, phone_number)
    if match:
        return True
    else:
        return False









