from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

import datetime as dt
import os

# Current weather, minute forecast for 1 hour, hourly forecast for 48 hours,
# daily forecast for 7 days, historical data for 5 previous days for any location
# https://github.com/csparpa/pyowm
# https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#owm-weather-api-version-2-5-usage-examples


def current_weather(place='Novosibirsk'):
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM(os.environ['API_KEY_WEATHER'], config_dict)

        # Search for current weather in place
        weather_mgr = owm.weather_manager()
        geocode_mgr = owm.geocoding_manager()
        uvi_mgr = owm.uvindex_manager()

        # Get weather
        weather = weather_mgr.weather_at_place(place).current_weather
        # geocode town - get lat and lon
        list_of_locations = geocode_mgr.geocode(place, country='RU', limit=1)
        a_town = list_of_locations[0]
        lat = a_town.lat
        lon = a_town.lon
        # get uvi
        uvi = uvi_mgr.uvindex_around_coords(lat, lon)
    except Exception as e:
        print(repr(e))
        return None

    return_dict = {}
    return_dict['time'] = weather.reference_time(timeformat='date') + dt.timedelta(hours=7)
    return_dict['temperature'] = weather.temperature('celsius')['temp']
    return_dict['temperature_feel'] = weather.temperature('celsius')['feels_like']
    return_dict['wind'] = weather.wind()['speed']
    return_dict['pressure'] = weather.barometric_pressure()['press'] * 0.750               # Convert to mmHg
    return_dict['sunrise'] = weather.sunrise_time(timeformat='date') + dt.timedelta(hours=7)
    return_dict['sunset'] = weather.sunset_time(timeformat='date') + dt.timedelta(hours=7)
    return_dict['uv_val'] = uvi.value

    return return_dict


# def forecast_weather(place_fc='Novosibirsk'):
#     # forecast
#     try:
#         owm = OWM(os.environ['API_KEY_WEATHER'], language='ru')
#         # Query for 3 hours weather forecast for the next 5 days
#         fc_3h = owm.three_hours_forecast(place_fc)
#
#     except Exception as e:
#         print(repr(e))
#         return None
#
#     forecast_3h = fc_3h.get_forecast()
#
#     # Get the list of Weather objects...
#     # lst = forecast_3h.get_weathers()
#     # ...or iterate directly over the Forecast object
#     return_dict = {'time': [],
#                    'temperature': [],
#                    'wind': [],
#                    'pressure': [],
#                    'detailed_status': []}
#     for weather_ in forecast_3h:
#         ref_time = dt.datetime.fromtimestamp(weather_.get_reference_time())
#         return_dict['time'].append(ref_time)  # Время в Нск относительно  UTC
#         return_dict['temperature'].append(weather_.get_temperature('celsius')['temp'])
#         return_dict['wind'].append(weather_.get_wind()['speed'])
#         return_dict['pressure'].append(int(weather_.get_pressure()['press'] / 1.33322))
#         return_dict['detailed_status'].append(weather_.get_detailed_status())
#
#     # When in time does the forecast begin?
#     fc_3h.when_starts('date')  # datetime.datetime instance
#     # ...and when will it end?
#     fc_3h.when_ends('date')  # datetime.datetime instance
#
#     return return_dict
#
#
# # Возвращает четыре значения для каждого дня: ночь, утро, день, вечер
# def forecast_weather_sparse_dict(place_sp='Novosibirsk'):
#     weather_dict = forecast_weather(place_sp)
#
#     if weather_dict is None:
#         return None
#
#     return_dict_sparse = {'day': [],
#                           'month': [],
#                           'day_time': [],
#                           'temperature': [],
#                           'wind': [],
#                           'detailed_status': []}
#     for i in range(len(weather_dict['time'])):
#         if weather_dict['time'][i].hour == 4 or weather_dict['time'][i].hour == 7 or \
#                 weather_dict['time'][i].hour == 13 or weather_dict['time'][i].hour == 22:
#             return_dict_sparse['day'].append(weather_dict['time'][i].day)
#             return_dict_sparse['month'].append(weather_dict['time'][i].month)
#             return_dict_sparse['temperature'].append(weather_dict['temperature'][i])
#             return_dict_sparse['wind'].append(weather_dict['wind'][i])
#             return_dict_sparse['detailed_status'].append(weather_dict['detailed_status'][i])
#
#         if weather_dict['time'][i].hour == 4:
#             return_dict_sparse['day_time'].append("Ночь")
#         elif weather_dict['time'][i].hour == 7:
#             return_dict_sparse['day_time'].append("Утро")
#         elif weather_dict['time'][i].hour == 13:
#             return_dict_sparse['day_time'].append("День")
#         elif weather_dict['time'][i].hour == 22:
#             return_dict_sparse['day_time'].append("Вечер")
#     return return_dict_sparse
#
#
# # Возвращает список значение для вывода
# def forecast_weather_sparse_list(place_ls='Novosibirsk'):
#     sparse_dict = forecast_weather_sparse_dict(place_ls)
#     # if sparse_dict is None:
#     #     return None
#
#     ret_list = []
#     for count in range(0, len(sparse_dict["day"]) - 1, 4):
#         ret_list.append("{0}-{1}\n{2} t:{3} {4}\n{5} t:{6} {7}\n{8} t:{9} {10}\n{11} t:{12} {13}\n".format(
#             str(sparse_dict["day"][count]),
#             str(sparse_dict["month"][count]),
#             sparse_dict["day_time"][count],
#             str(int(sparse_dict["temperature"][count])),
#             sparse_dict["detailed_status"][count],
#             sparse_dict["day_time"][count + 1],
#             str(int(sparse_dict["temperature"][count + 1])),
#             sparse_dict["detailed_status"][count + 1],
#             sparse_dict["day_time"][count + 2],
#             str(int(sparse_dict["temperature"][count + 2])),
#             sparse_dict["detailed_status"][count + 2],
#             sparse_dict["day_time"][count + 3],
#             str(int(sparse_dict["temperature"][count + 3])),
#             sparse_dict["detailed_status"][count + 3]))
#
#     return ret_list


if __name__ == '__main__':
    place = "Novosibirsk"
    weath_dict = current_weather(place)
    print(weath_dict)

    str = f"""Погода на: {weath_dict['time'].strftime('%Y-%m-%d %H:%M:%S')}
{place}
Температура: {weath_dict['temperature']} C,
Ощущается: {weath_dict['temperature_feel']} C,
Давление: {weath_dict['pressure']} мм.рт.ст,
Ветер: {weath_dict['wind']} м/с, 
UV-индекс: {weath_dict['uv_val']},
Восход: {weath_dict['sunrise'].strftime('%H:%M:%S')},
Закат: {weath_dict['sunset'].strftime('%H:%M:%S')}
    """
    print(str)
    # rt_lst = forecast_weather_sparse_list(place)
    #
    # print(rt_lst[0])
    # # print(rt_lst[1])
    # # print(rt_lst[2])
    # # print(rt_lst[3])
    # # print(rt_lst[4])

