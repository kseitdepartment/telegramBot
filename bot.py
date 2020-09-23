import requests

from bs4 import BeautifulSoup
from aiogram.dispatcher.filters import Command
from choice_buttons import choice
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, executor

from config import BOT_TOKEN
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(Command("start"))
async def process_start_command(message: Message):
    await message.reply("Здравстуйте!\n Чтобы вызвать помощь,напишите /help")


@dp.message_handler(Command("help"))
async def process_help_command(message: Message):
    await message.reply("Напишите мне /getinfo,чтобы вызвать информационную панель")


@dp.message_handler(Command("getinfo"))
async def process_start_getinfo(message: Message):
    await message.answer(text="Выберите из списка необходимую опцию \n",
                         reply_markup=choice)


@dp.callback_query_handler(text_contains="btn1")
async def process_callback(call: CallbackQuery):
    await call.answer(cache_time=60)

    url = 'https://www.kse.kg/ru/Quotes'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    line = soup.find('table', class_='class1').find_all('tr', class_='parse')

    data = []

    for tr in line:
        td = tr.find_all('td')
        name = td[2].text
        sell = td[4].text
        buy = td[6].text

        if not sell:
            data = {
                '<b>\U0001F9F0 Наименование</b>': name,
                '<b>\u2757\uFE0F Покупка</b>': buy
            }

        if not buy:
            data = {
                '<b>\U0001F9F0 Наименование</b>': name,
                '<b>\u203C Продажа</b>': sell
            }

        await call.message.answer(str(data))
if __name__ == '__main__':
    executor.start_polling(dp)
