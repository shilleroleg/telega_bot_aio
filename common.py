from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Офигенски, погнали!", reply_markup=types.ReplyKeyboardRemove())


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def cmd_help(message: types.Message, state: FSMContext):
    await state.finish()
    help_ans = """Доступные комманды:
стикер - посылает случайный стикер.
погода - погода на данный момент.
прогноз - прогноз погоды на 5 дней.
курс - курс валют"""
    await message.answer(help_ans, reply_markup=types.ReplyKeyboardRemove())


async def cmd_hello(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_help, Text(equals="справка", ignore_case=True), state="*")
    dp.register_message_handler(cmd_hello, commands="hello", state="*")
    dp.register_message_handler(cmd_hello, Text(equals="привет", ignore_case=True), state="*")

