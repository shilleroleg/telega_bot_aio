import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from weather import register_handlers_weather
from common import register_handlers_common
from currency import register_handlers_currency


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
