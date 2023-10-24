from aiogram import Bot, types, executor, Dispatcher
import logging

from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def start(msg: types.Message):
    text = f"Assalomu alekum {msg.from_user.full_name} bizning botimizga hush kelibsiz!"
    await msg.answer(text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)