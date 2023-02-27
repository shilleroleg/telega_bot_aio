from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import get_currencies


def currensy_ans():
    curr = get_currencies.get_currencies_pair()
    return f"""Курс валют на: {curr['time']}
Доллар: {curr['usd']}
Евро: {curr['eur']}
Юань: {curr['cny']}
Фунт: {curr['gbp']}
Гривна: {curr['uah']}
Бел.руб.: {curr['byn']}
Биткоин: {curr['btc']}$
"""


async def currency_start(message: types.Message):
    answer_text = currensy_ans()

    await message.answer(answer_text)


def register_handlers_currency(dp: Dispatcher):
    dp.register_message_handler(currency_start, commands="currency", state="*")
    dp.register_message_handler(currency_start, Text(equals="курс", ignore_case=True), state="*")
    dp.register_message_handler(currency_start, Text(equals="валюта", ignore_case=True), state="*")