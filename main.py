from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

API_TOKEN = '8183661988:AAHucFqlurcSvaLbkD8ZyI0-JAYSsF6xU_U'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def start_handler(message: types.Message):
    await message.answer("Привет, братец! Я Санин первый бот 🤖, это чисто тестик")

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")

async def main():
    await dp.start_polling(bot)  # <- передаем bot сюда!

if __name__ == "__main__":
    asyncio.run(main())