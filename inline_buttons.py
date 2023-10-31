from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikm = InlineKeyboardMarkup(row_width=2)
i1 = InlineKeyboardButton(text='HA', callback_data='yes')
i2 = InlineKeyboardButton(text="Yo'q", callback_data='no')
ikm.add(i1, i2)
