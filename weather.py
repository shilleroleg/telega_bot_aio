from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from helper_func import weather_ans

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_town_names = ["Новосибирск", "Красноярск", "Другой"]


class SelectTown(StatesGroup):
    waiting_for_town_name = State()
    waiting_for_other_name = State()


async def town_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_town_names:
        keyboard.add(name)
    await message.answer("Выберите город:", reply_markup=keyboard)
    await state.set_state(SelectTown.waiting_for_town_name.state)


async def town_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_town_names:
        await message.answer("Пожалуйста, выберите город, используя клавиатуру ниже.")
        return
    elif message.text.lower() == 'другой':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Ок')
        await state.set_state(SelectTown.waiting_for_other_name.state)
        await message.answer("Выберите другой город:", reply_markup=keyboard)

    await state.update_data(chosen_town=message.text.lower())


async def other_town_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    answer_str = weather_ans(user_data.get('chosen_town'))

    await message.answer(answer_str, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(town_start, commands="weather", state="*")
    dp.register_message_handler(town_start, Text(equals="погода", ignore_case=True), state="*")
    dp.register_message_handler(town_chosen, state=SelectTown.waiting_for_town_name)
    dp.register_message_handler(other_town_chosen, state=SelectTown.waiting_for_other_name)
