from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import token_weather
import requests
import datetime


TOKEN_API = "6218547706:AAF1HdzuxIrNwX8CSNwiWsBdD2CSkQ6broU"

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('/help'))

Choice = """
/general_weather - общая погода на данный момент
/weather_for_half_a_day - погода на пол дня
/weather_for_the_day - погода на сутки 
"""

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот был успешно запущен')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Напиши команду /help для ориентации в боте",
                         reply_markup=kb)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=Choice,
                         reply_markup=ReplyKeyboardRemove())

@dp.message_handler()
async def heart(message: types.Message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F328"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token_weather}&units=metric"
        )
        data = r.json()

        city = data["name"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму, что за погода!"

        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        feels_lake = data["main"]["feels_like"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Ощущается: {feels_lake}C°\nВлажность: {humidity}%\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise}\nЗакат солнца: {sunset}\n"
                            f"***Хорошего дня!***")
    except:
        await message.reply("\U00002620 проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
