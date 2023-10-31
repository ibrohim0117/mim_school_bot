from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    first_name = State()
    age = State()
    phone_number = State()


class Fedbik(StatesGroup):
    content = State()


class SendMessageUsers(StatesGroup):
    text_user = State()
    photo = State()
    yes_or_no = State()













