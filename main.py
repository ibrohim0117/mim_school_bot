from aiogram import Bot, types, executor, Dispatcher
import logging
from config import TOKEN, ID1
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from defoult_buttons import btn, contact
from states import Reg, Fedbik

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=MemoryStorage())

username = ''

@dp.message_handler(commands="start")
async def start(msg: types.Message):
    text = f"Assalomu alekum {msg.from_user.full_name} bizning botimizga hush kelibsiz!"
    a = (msg.from_user.id)
    print(a)
    await msg.answer(text, reply_markup=btn)


@dp.message_handler(text='🏢Bizning joylashuv')  # noqa
async def locotion(msg: types.Message):
    text = """
     📍Manzil: Qorasuv mavzesi 12A uy
    🏬Mo'ljal: Al Eayila do'koni 2-qavat
    """
    await msg.answer(text)
    await bot.send_location(msg.from_user.id, longitude=66.933566, latitude=39.718122)


@dp.message_handler(text='📞Admin bilan aloqa')
async def aloqa(msg: types.Message):
    await bot.send_contact(msg.from_user.id, phone_number=" +998 78 1131551", first_name='Admin')


@dp.message_handler(text="🚀Kurslarga yozilish / to'liq ma'lumot olish")
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
    text = f" Mijozning ismi: {s.get('first_name')}\n" \
           f"Mijozning yoshi: {s.get('age')}\n" \
           f"Mijozning telefon raqami: {s.get('phone_number')}"
    await bot.send_message(ID1, text)
    await msg.answer("Tez orada siz bilan bog'lanamiz...")
    await state.finish()


@dp.message_handler(text='✉️Talab va takliflar uchun')
async def fedbik(msg: types.Message):
    text = """
    O'quv markazimiz o'quvchilari markazimiz sharoitlari haqidagi va o'qituvchilar yoki dars jarayonidagi
    kamchiliklar haqidagi har qanday talab va takliflarni tinglashga tayyormiz!
    Shaxsingiz to'liq sir saqlanadi!
    """
    await msg.answer(text)
    await msg.answer("Izohni qoldiring:  ")
    await Fedbik.content.set()


@dp.message_handler(state=Fedbik.content)
async def content(msg: types.Message, state: FSMContext):
    username = msg.from_user.username
    await state.update_data(cotent=msg.text)
    s = await state.get_data()
    text = f"Izoh: {s['cotent']}\n" \
           f"User: @{username}"
    await bot.send_message(ID1, text)
    await msg.answer("Qabul qilindi sizning fikringiz biz uchun muhum!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)