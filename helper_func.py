import currencies
import getweather

def currensy_ans():
    curr = currencies.get_currencies_pair()
    return f"""Курс валют на: {curr['time']}
Доллар: {curr['usd']}
Евро: {curr['eur']}
Юань: {curr['cny']}
Фунт: {curr['gbp']}
Гривна: {curr['uah']}
Бел.руб.: {curr['byn']}
Биткоин: {curr['btc']}$"""


def help_ans():
    return """
Доступные комманды:
стикер - посылает случайный стикер.
погода - погода на данный момент.
прогноз - прогноз погоды на ближайшие 5 дней.
курс - курс валют"""


def weather_ans(place='Novosibirsk'):
    weath_dict = getweather.current_weather(place)
    return f"""Погода на: {weath_dict['time'].strftime('%Y-%m-%d %H:%M:%S')}
{place}
Температура: {weath_dict['temperature']} C,
Ощущается: {weath_dict['temperature_feel']} C,
Давление: {weath_dict['pressure']} мм.рт.ст,
Ветер: {weath_dict['wind']} м/с, 
UV-индекс: {weath_dict['uv_val']},
Восход: {weath_dict['sunrise'].strftime('%H:%M:%S')},
Закат: {weath_dict['sunset'].strftime('%H:%M:%S')}
    """