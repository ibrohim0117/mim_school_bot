from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

b1 = KeyboardButton(text="🚀Kurslarga yozilish / to'liq ma'lumot olish")
b2 = KeyboardButton(text='🏢Bizning joylashuv')
b3 = KeyboardButton(text='📞Admin bilan aloqa')
b4 = KeyboardButton(text='✉️Talab va takliflar uchun')


btn.add(b1, b2, b3, b4)
contact = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
c2 = KeyboardButton(text="Telefon raqmni ulashish", request_contact=True)
contact.add(c2)