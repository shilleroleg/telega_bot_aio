import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weather import register_handlers_weather
from common import register_handlers_common
from currency import register_handlers_currency

from helper_func import currensy_ans, help_ans, weather_ans

TOKEN = os.environ['TOKEN_TELEGRAM']

WEBHOOK_HOST = f'https://oracle-telegram-bot.onrender.com'
WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Объект бота
bot = Bot(TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers_weather(dp)
register_handlers_currency(dp)
register_handlers_common(dp)


# @dp.message_handler(content_types=['text'])
# async def send_text(message):
#     if message.text.lower() == "привет":  # Отвечает на сообщение
#         answer_text = f'Привет,  {message.from_user.first_name}'
#
#     # elif message.text.lower() == "стикер":          # Отправляет стикер в ответ  на сообщение
#     #     bot.send_sticker(message.chat.id, choice(stickerlist.sticker_list))
#     #
#     # elif message.text.lower() == "погода":
#     #     keyboard = InlineKeyboardMarkup(row_width=2)
#     #     item1 = InlineKeyboardButton("Новосибирск", callback_data='Nsk')
#     #     item2 = InlineKeyboardButton("Другой город", callback_data='Other')
#     #     keyboard.add(item1, item2)
#     #
#     #     await message.answer("Где смотрим погоду?", reply_markup=keyboard)
#
#     # elif message.text.lower() == "прогноз":
#     #     rt_lst = getw.forecast_weather_sparse_list("Novosibirsk")
#     #
#     #     bot.send_message(message.chat.id, rt_lst[0])
#     #     # bot.send_message(message.chat.id, rt_lst[1])
#     #     # bot.send_message(message.chat.id, rt_lst[2])
#     #     # bot.send_message(message.chat.id, rt_lst[3])
#     #     # bot.send_message(message.chat.id, rt_lst[4])
#     elif message.text.lower() == "курс":
#         answer_text = currensy_ans()
#
#     else:
#         answer_text = f'Я запомню\n{message.text}'
#
#     await message.answer(answer_text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()


if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port='8000',
    )
