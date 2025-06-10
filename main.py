import aiohttp
import xml.etree.ElementTree as ET

API_TOKEN = '8183661988:AAHucFqlurcSvaLbkD8ZyI0-JAYSsF6xU_U'
OWM_API_KEY = '0e0a1bb742bef256373c62e7661ca79a'

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_names = {}

@dp.message(Command(commands=["start"]))
async def start_handler(message: types.Message):
    await message.answer("Привет! Как тебя зовут?")

@dp.message()
async def name_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_names:
        user_names[user_id] = message.text
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Погода в Москве")],
                [KeyboardButton(text="Курс валют")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer(f"Приятно познакомиться, {message.text}! Что хочешь узнать?", reply_markup=keyboard)
    else:
        choice = message.text.lower()
        if "погода" in choice:
            weather = await get_weather()
            await message.answer(weather)
        elif "курс" in choice:
            rates = await get_exchange_rates()
            usd = rates.get("USD", "Нет данных")
            eur = rates.get("EUR", "Нет данных")
            await message.answer(f"Курс доллара: {usd} рублей\nКурс евро: {eur} рублей")
        else:
            await message.answer("Пожалуйста, выбери одну из кнопок.")

async def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OWM_API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data.get("cod") != 200:
                return "Не удалось получить погоду."
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            return f"Погода в Москве: {desc}, температура {temp}°C"

async def get_exchange_rates():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            root = ET.fromstring(text)
            rates = {}
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                value = valute.find('Value').text
                nominal = valute.find('Nominal').text
                rates[char_code] = float(value.replace(',', '.')) / int(nominal)
            return rates

if __name__ == "__main__":
    asyncio.run(dp.start_polling())