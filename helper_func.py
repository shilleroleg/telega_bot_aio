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
    weath_dict = getweather.weather(place)
    str0 = place + " {0}\n".format(str(weath_dict['time']))

    str1 = "Температура: {0} C\nВлажность: {1}%\n".format(str(weath_dict['temperature']),
                                                          str(weath_dict['humidity']))
    str2 = "Давление {0} мм.рт.ст\nВетер: {1} м/с\n".format(str(int(weath_dict['pressure'] / 1.33322)),
                                                            str(weath_dict['wind']))
    str3 = "UV-индекс: {0}\nUV-риск: {1}\n".format(str(weath_dict['uv_val']),
                                                   str(weath_dict['uv_risk']))
    return str0 + str1 + str2 + str3