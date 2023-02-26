import asyncio

from aiogram import Bot, Dispatcher, executor, types

import currencies
import config

# Объект бота
bot = Bot(config.TOKEN_TELEGRAM)
# Диспетчер
dp = Dispatcher(bot)


# Хэндлер на команду /start
@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    answer_text = ''
    if message.text == '/start':
        answer_text = "Офигенски, погнали!"
    elif message.text == '/help':
        answer_text = """
Доступные комманды:
стикер - посылает случайный стикер.
погода - погода на данный момент.
прогноз - прогноз погоды на ближайшие 5 дней.
курс - курс валют"""

    await message.answer(answer_text)


@dp.message_handler(content_types=['text'])
async def send_text(message):
    if message.text.lower() == "привет":           # Отвечает на сообщение
        answer_text = f'Привет,  {message.from_user.first_name}'

    # elif message.text.lower() == "стикер":          # Отправляет стикер в ответ  на сообщение
    #     bot.send_sticker(message.chat.id, choice(stickerlist.sticker_list))
    #
    # elif message.text.lower() == "погода":
    #     keyboard = tb.types.InlineKeyboardMarkup(row_width=2)
    #     item1 = tb.types.InlineKeyboardButton("Новосибирск", callback_data='Nsk')
    #     item2 = tb.types.InlineKeyboardButton("Другой город", callback_data='Other')
    #     keyboard.add(item1, item2)
    #
    #     bot.send_message(message.chat.id, "Где смотрим погоду?", reply_markup=keyboard)

    # elif message.text.lower() == "прогноз":
    #     rt_lst = getw.forecast_weather_sparse_list("Novosibirsk")
    #
    #     bot.send_message(message.chat.id, rt_lst[0])
    #     # bot.send_message(message.chat.id, rt_lst[1])
    #     # bot.send_message(message.chat.id, rt_lst[2])
    #     # bot.send_message(message.chat.id, rt_lst[3])
    #     # bot.send_message(message.chat.id, rt_lst[4])
    elif message.text.lower() == "курс":
        curr = currencies.get_currencies_pair()
        answer_text = f"""Курс валют на: {curr['time']}
Доллар: {curr['usd']}
Евро: {curr['eur']}
Юань: {curr['cny']}
Фунт: {curr['gbp']}
Гривна: {curr['uah']}
Бел.руб.: {curr['byn']}
Биткоин: {curr['btc']}$"""

    else:
        answer_text = f'Я запомню\n{message.text}'

    await message.answer(answer_text)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f'Я запомню\n{message.text}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
