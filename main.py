import aiogram.utils.markdown as md
from aiogram import Bot, types, executor, Dispatcher
import logging
from config import TOKEN, ID1, ID2, ID3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ParseMode
from database import creat_table, insert_into, check_user, user_list
from defoult_buttons import btn, contact
from inline_buttons import ikm
from states import Reg, Fedbik, SendMessageUsers
from utils import validate_phone_number


logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=MemoryStorage())

username = ''


@dp.message_handler(commands="start")
async def start(msg: types.Message):
    creat_table()
    text = "Assalomu alekum botimizga hush kelibsiz!"
    if check_user(msg.from_user.id):
        await msg.answer(text, reply_markup=btn)
    else:
        await insert_into(str(msg.from_user.id), msg.from_user.username, msg.from_user.full_name)
        await msg.answer(text, reply_markup=btn)


@dp.message_handler(text='🏢Bizning joylashuv')  # noqa
async def locotion(msg: types.Message):
    text = """
📍Manzil: Qorasuv mavzesi 12A uy
🏬Mo'ljal: Al Eayila do'koni 2-qavat
    """
    await msg.answer(f"<b>{text}</b>", parse_mode='html')
    await bot.send_location(msg.from_user.id, longitude=66.933566, latitude=39.718122)


@dp.message_handler(text='📞Admin bilan aloqa')
async def aloqa(msg: types.Message):
    await bot.send_contact(msg.from_user.id, phone_number=" +998 78 1131551", first_name='Admin')


@dp.message_handler(text="🚀Kurslarga yozilish / to'liq ma'lumot olish")
async def first_name(msg: types.Message):
    text = "Ismingizni kiriting: "
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())
    await Reg.first_name.set()


@dp.message_handler(state=Reg.first_name)
async def name(msg: types.Message, state: FSMContext):
    await state.update_data(first_name=msg.text)
    text = "Yoshingizni kiriting: "
    await msg.answer(text)
    await Reg.age.set()


@dp.message_handler(state=Reg.age)
async def age(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(age=msg.text)
        text = "Telfon raqamingizni kiriting: "
        await msg.answer(text, reply_markup=contact)
        await Reg.phone_number.set()
    else:
        await msg.answer('Yoshingizni raqam shakilda kirting!')
        await msg.answer("Yoshingizni kiriting: ")


@dp.message_handler(state=Reg.phone_number, content_types=types.ContentTypes.CONTACT)
async def phone_number(msg: types.Message, state: FSMContext):
    # print(msg.text)
    await state.update_data(phone_number=msg.contact.phone_number)
    s = await state.get_data()  # noqa
    text = f" Mijozning ismi: {s.get('first_name')}\n" \
           f"Mijozning yoshi: {s.get('age')}\n" \
           f"Mijozning telefon raqami: {s.get('phone_number')}"
    await bot.send_message(ID1, text)
    await msg.answer("Tez orada siz bilan bog'lanamiz...", reply_markup=btn)
    await state.finish()


@dp.message_handler(state=Reg.phone_number)
async def phone_number(msg: types.Message, state: FSMContext):
    if validate_phone_number(msg.text):
        await state.update_data(phone_number=msg.text)
        s = await state.get_data()
        text = f" Mijozning ismi: {s.get('first_name')}\n" \
               f"Mijozning yoshi: {s.get('age')}\n" \
               f"Mijozning telefon raqami: {s.get('phone_number')}"
        await bot.send_message(ID1, text)
        await msg.answer("Tez orada siz bilan bog'lanamiz...", reply_markup=btn)
        await state.finish()
    else:
        await msg.answer("Telefon raqamni qaytadan  to'g'ri kiriting!")


@dp.message_handler(text='✉️Talab va takliflar uchun')
async def fedbik(msg: types.Message):
    text = """
O'quv markazimiz o'quvchilari markazimiz sharoitlari yoki dars jarayonidagi
kamchiliklar haqidagi. Har qanday talab va takliflarni tinglashga tayyormiz!
Shaxsingiz to'liq sir saqlanadi!"""
    await msg.answer(f"<b>{text}</b>", parse_mode='html')
    await msg.answer("Izohni qoldiring:  ", reply_markup=ReplyKeyboardRemove())
    await Fedbik.content.set()


@dp.message_handler(state=Fedbik.content)
async def content(msg: types.Message, state: FSMContext):
    username = msg.from_user.username
    await state.update_data(cotent=msg.text)
    s = await state.get_data()
    text = f"Izoh: {s['cotent']}\n" \
           f"User: @{username}"
    await bot.send_message(ID3, text)
    await state.finish()
    await msg.answer(f"<b>Qabul qilindi sizning fikringiz biz uchun muhum!</b>", parse_mode='html', reply_markup=btn)


@dp.message_handler(text="h@bar#yuborish")
async def message(msg: types.Message):
    if msg.from_user.id == ID1:
        await SendMessageUsers.text_user.set()
        await msg.answer("Xabarni kiriting: ")
    else:
        await msg.answer('Buttonslardan birini tanlang!')


@dp.message_handler(state=SendMessageUsers.text_user)
async def l_h(msg: types.Message, state: FSMContext):
    # print(msg.text)
    await state.update_data(text_user=msg.text)
    await msg.answer('Habarning rasmini kiriting: ')
    await SendMessageUsers.photo.set()


@dp.message_handler(state=SendMessageUsers.photo, content_types=types.ContentType.PHOTO)
async def get_photo_handler(msg: types.Message, state: FSMContext):
    await state.update_data({"photo": msg.photo[-1].file_id})
    text = "<b>Habar yuborilsinmi?</b>"
    await msg.answer(text=text, reply_markup=ikm, parse_mode='html')
    await SendMessageUsers.yes_or_no.set()


@dp.callback_query_handler(text=(['yes', 'no']), state=SendMessageUsers.yes_or_no)
async def yes_handler_h(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(yes_no=callback.data)
    s = await state.get_data()
    photo = s['photo']
    text = s['text_user']
    await state.finish()
    if callback.data == 'yes':
        if callback.from_user.id == ID1 or callback.from_user.id == ID2:
            try:
                for i in user_list():
                    await bot.send_photo(chat_id=int(i), caption=text, photo=photo)
                await callback.answer("Habar yuborildi!")
            except:  # noqa
                pass
    else:
        await callback.message.answer('Amalyot bekor qilindi!')


async def on_startup(dp):
    creat_table()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
