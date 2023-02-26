import asyncio

from aiogram import Bot, Dispatcher, executor, types

import config


# Объект бота
bot = Bot(config.TOKEN_TELEGRAM)
# Диспетчер
dp = Dispatcher(bot)


# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    