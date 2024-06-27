import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY

bot = Bot(token=TOKEN)
bot_1 = Bot(token=WEATHER_API_KEY)



dp = Dispatcher()


# Функция для получения прогноза погоды
async def get_weather(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200:
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                return f'Погода в городе {city}: {weather}, температура: {temp}°C'
            else:
                return 'Не удалось получить прогноз погоды. Проверьте название города.'


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот передаёт прогноз погоды. Используйте команду /weather <город> для получения прогноза.')


@dp.message(CommandStart)
async def start(message: Message):
    await message.answer('Привет! Я бот! Используйте команду /weather <город> для получения прогноза погоды.')


@dp.message(Command('weather'))
async def weather(message: Message):
    city = message.get_args()
    if not city:
        await message.answer('Пожалуйста, укажите город после команды /weather. Например: /weather Москва')
        return

    weather_report = await get_weather(city)
    await message.answer(weather_report)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())