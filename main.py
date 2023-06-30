import requests
import datetime
from config import token_weather
from pprint import pprint

def get_weather(city, token_weather):

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
        #f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token_weather}&units=metric"
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token_weather}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data['city']["name"]

        for i in range(8):
            weather_description = data['list'][i]["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму, что за погода!"

            cur_weather = data['list'][i]['main']['temp']
            humidity = data['list'][i]['main']['humidity']
            feels_lake = data['list'][i]['main']['feels_like']
            wind = data['list'][i]['wind']['speed']
            time_now = data['list'][i]['dt_txt']

            print(f"***{time_now}***\n"
                  f"Температура: {cur_weather}C° {wd}\n"
                  f"Ощущается: {feels_lake}C°\nВлажность: {humidity}%\nВетер: {wind} м/с\n")

    except Exception as ex:
        print(ex)
        print("проверьте название города")

def main():
    city = input("Введите город: ")
    #token_weather = "a2b844121555ec6a00248ebba4da337b"
    get_weather(city, token_weather)

if __name__ == '__main__':
    main()
