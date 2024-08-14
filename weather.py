from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from get_weather import current_weather, forecast_weather

available_town_names = ["Санкт-Петербург", "Москва", "Новосибирск", "Другой"]


class SelectTown(StatesGroup):
    waiting_for_town_name = State()
    waiting_for_other_name = State()


async def town_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_town_names:
        keyboard.add(name)
    await message.answer("Выберите город:", reply_markup=keyboard)

    async with state.proxy() as data:
        data['command'] = 'weather'

    await SelectTown.waiting_for_town_name.set()


async def town_start_forecast(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_town_names:
        keyboard.add(name)
    await message.answer("Выберите город:", reply_markup=keyboard)

    async with state.proxy() as data:
        data['command'] = 'forecast'

    await SelectTown.waiting_for_town_name.set()


async def town_chosen_invalid(message: types.Message):
    return await message.reply("Неверное название города. Выберите город из списка")


async def town_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() == 'другой':
        await state.set_state(SelectTown.waiting_for_other_name.state)
        await message.answer("Введите название города:", reply_markup=types.ReplyKeyboardRemove())
    else:
        async with state.proxy() as data:
            data['town'] = message.text

        user_data = await state.get_data()
        if user_data.get('command') == 'weather':
            ans_str = current_weather(user_data.get('town'))
        elif user_data.get('command') == 'forecast':
            ans_str = forecast_weather(user_data.get('town'))
        else:
            ans_str = ''
        await message.answer(ans_str, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


async def other_town_chosen(message: types.Message, state: FSMContext):
    # Update state and data
    await SelectTown.next()
    await state.update_data(town=message.text)

    user_data = await state.get_data()
    try:
        if user_data.get('command') == 'weather':
            ans_str = current_weather(user_data.get('town'))
        elif user_data.get('command') == 'forecast':
            ans_str = forecast_weather(user_data.get('town'))
        else:
            ans_str = ''
        await message.answer(ans_str, reply_markup=types.ReplyKeyboardRemove())
    except:
        ans_str = "Что-то пошло не так. Возможно, ошибка в названии города"
        await message.reply(ans_str, reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(town_start, commands="weather", state="*")
    dp.register_message_handler(town_start, Text(equals="погода", ignore_case=True), state="*")
    dp.register_message_handler(town_start_forecast, commands="forecast", state="*")
    dp.register_message_handler(town_start_forecast, Text(equals="прогноз", ignore_case=True), state="*")
    dp.register_message_handler(town_chosen_invalid, lambda message: message.text not in available_town_names,
                                state=SelectTown.waiting_for_town_name)
    dp.register_message_handler(town_chosen, state=SelectTown.waiting_for_town_name)
    dp.register_message_handler(other_town_chosen, state=SelectTown.waiting_for_other_name)
