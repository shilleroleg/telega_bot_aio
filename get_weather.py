import os
import requests
from datetime import datetime, timedelta

import pandas as pd

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

# Current weather, minute forecast for 1 hour, hourly forecast for 48 hours,
# daily forecast for 7 days, historical data for 5 previous days for any location
# https://github.com/csparpa/pyowm
# https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#owm-weather-api-version-2-5-usage-examples


def current_weather(place: str = 'Novosibirsk') -> str:
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM(os.environ['API_KEY_WEATHER'], config_dict)

        # Search for current weather in place
        weather_mgr = owm.weather_manager()
        geocode_mgr = owm.geocoding_manager()
        uvi_mgr = owm.uvindex_manager()

        # Get weather
        weather = weather_mgr.weather_at_place(place).weather
        # geocode town - get lat and lon
        list_of_locations = geocode_mgr.geocode(place, country='RU', limit=1)
        a_town = list_of_locations[0]
        lat = a_town.lat
        lon = a_town.lon
        # get uvi
        uvi = uvi_mgr.uvindex_around_coords(lat, lon)
    except Exception as e:
        return 'Ошибка при получении погоды'

    return_dict = {'place': place,
                   'time': weather.reference_time(timeformat='date') + timedelta(hours=3),
                   'temperature': weather.temperature('celsius')['temp'],
                   'temperature_feel': weather.temperature('celsius')['feels_like'],
                   'wind': weather.wind()['speed'],
                   'pressure': weather.barometric_pressure()['press'] * 0.750,
                   'sunrise': weather.sunrise_time(timeformat='date') + timedelta(hours=3),
                   'sunset': weather.sunset_time(timeformat='date') + timedelta(hours=3),
                   'uv_val': uvi.value}

    return format_out_str_weather(return_dict)


def forecast_weather(place: str = 'Moscow') -> str:
    api_key = os.environ['API_KEY_WEATHER']
    error_msg = 'Ошибка. Попробуйте позже'
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM(api_key, config_dict)

        # Search for current weather in place
        geocode_mgr = owm.geocoding_manager()
        list_of_locations = geocode_mgr.geocode(place, country='RU', limit=1)
        a_town = list_of_locations[0]
        lat = a_town.lat
        lon = a_town.lon
    except:
        return error_msg

    api_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'

    r = requests.get(api_url)

    if r.status_code == 200:
        answer_list = r.json().get('list')
        weather_df = parse_weather_forecast(answer_list)
        weather_df_units = change_units(weather_df)
        grouped_forecast = group_by_day(weather_df_units)
        # print(grouped_forecast)
        out_str = format_out_str_forecast(grouped_forecast)
        return out_str
    else:
        return error_msg


def parse_weather_forecast(weathers_list: list[dict]) -> pd.DataFrame:
    out_df = pd.DataFrame()
    for weather in weathers_list:
        all_df = [pd.DataFrame.from_dict(weather['main'], orient='index').T,
                  pd.DataFrame.from_dict(weather['wind'], orient='index').T]

        df_row = pd.concat(all_df, axis=1)
        df_row['dt'] = datetime.fromtimestamp(weather['dt'])
        df_row['date_'] = pd.to_datetime(df_row['dt']).dt.date
        # Find part of the day
        hour_ = pd.to_datetime(df_row['dt']).dt.hour
        df_row['daytime'] = 'День' if 8 <= hour_[0] < 20 else 'Ночь'

        out_df = pd.concat([out_df, df_row])
    return out_df


def change_units(df_in: pd.DataFrame) -> pd.DataFrame:
    """

    """
    df_in['temp'] = df_in['temp'] - 273.15
    df_in['feels_like'] = df_in['feels_like'] - 273.15
    df_in['pressure'] = df_in['pressure'] / 1.33322

    df_in['date_'] = pd.to_datetime(df_in['dt']).dt.date

    return df_in


def group_by_day(df_in: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (df_in
                  .groupby(['date_', 'daytime'])
                  .agg({'temp': 'mean',
                        'feels_like': 'mean',
                        'pressure': 'mean',
                        'humidity': 'mean',
                        'speed': 'mean'})
                  .rename({'speed': 'wind'})
                  .reset_index())
    return df_grouped


def format_out_str_weather(weath_dict: dict) -> str:
    return f"""Погода на: {weath_dict['time'].strftime('%Y-%m-%d %H:%M:%S')}
{weath_dict['place']}
Температура: {weath_dict['temperature']} C,
Ощущается: {weath_dict['temperature_feel']} C,
Давление: {weath_dict['pressure']} мм.рт.ст,
Ветер: {weath_dict['wind']} м/с, 
UV-индекс: {weath_dict['uv_val']},
-------
Восход: {weath_dict['sunrise'].strftime('%H:%M:%S')},
Закат: {weath_dict['sunset'].strftime('%H:%M:%S')}
"""


def format_out_str_forecast(df: pd.DataFrame) -> str:
    out_str = f"{'Дата':^5} | {'Время':^6} | {'t,C':^6} | {'Ощущается':^9} | {'Влажность':^10}\n"
    for _, row in df.iterrows():
        out_str += f"{row['date_']:%d.%m} | {row['daytime']:^6} | {row['temp']:^6.1f} | {row['feels_like']:^9.1f} | {row['humidity']:^10.0f}\n"
    return out_str


if __name__ == '__main__':
    #     place = "Novosibirsk"
    #     weath_dict = current_weather(place)
    #     print(weath_dict)
    #
    forecast_weather()

