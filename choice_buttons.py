from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Котировки \U0001F4CA', callback_data='btn1')

    ]
])

