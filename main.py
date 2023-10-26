from aiogram import Bot, types, executor, Dispatcher
import logging
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from defoult_buttons import btn, contact
from states import Reg

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def start(msg: types.Message):
    text = f"Assalomu alekum {msg.from_user.full_name} bizning botimizga hush kelibsiz!"
    await msg.answer(text, reply_markup=btn)


@dp.message_handler(text='Registratsiya')
async def first_name(msg: types.Message):
    text = "Ismingizni kiriting: "
    await msg.answer(text)
    await Reg.first_name.set()


@dp.message_handler(state=Reg.first_name)
async def name(msg: types.Message, state: FSMContext):
    await state.update_data(first_name=msg.text)
    text = "Yoshingizni kiriting: "
    await msg.answer(text)
    await Reg.age.set()


@dp.message_handler(state=Reg.age)
async def age(msg: types.Message, state: FSMContext):
    await state.update_data(age=msg.text)
    text = "Telfon raqamingizni kiriting: "
    await msg.answer(text, reply_markup=contact)
    await Reg.phone_number.set()


@dp.message_handler(state=Reg.phone_number, content_types=types.ContentTypes.CONTACT)
async def phone_number(msg: types.Message, state: FSMContext):
    await state.update_data(phone_number=msg.contact.phone_number)
    s = await state.get_data()
    text = f" Ismingiz: {s.get('first_name')}\n" \
           f"Yoshingiz: {s.get('age')}\n" \
           f"Telefon raqamingiz: {s.get('phone_number')}"
    await msg.answer(text)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)