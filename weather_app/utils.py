from urllib.request import urlopen
from json import load

import requests
from datetime import datetime

def ipInfo(addr=''):
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    data = load(res)
    return data['city']


def infoWeather(city):
    appid = 'ee42302f99f13c3576fe03395b7555ac'
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        print("Exception (find):", e)
        return '', ''
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'en', 'APPID': appid})
        data = res.json()
        now = (data['weather'][0]['description'], data['main']['temp'])
    except Exception as e:
        print("Exception (weather):", e)
        return '', ''
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'en', 'APPID': appid})
        data = res.json()
        forecast = []
        d = datetime.now()
        for i in data['list']:
            if i['dt_txt'][11:19] == '09:00:00':
                forecast.append(i['dt_txt'][8:10] + ' ' + d.strftime('%B') + '⠀—⠀'
                                + i['weather'][0]['description'] + ' (' + '{0:+3.0f}'.format(i['main']['temp']) + '°С')
            elif i['dt_txt'][11:19] == '18:00:00' and forecast:
                forecast[-1] = forecast[-1] + ', ' + '{0:+3.0f}'.format(i['main']['temp']) + '°С)'
    except Exception as e:
        print("Exception (forecast):", e)
        return '', ''
    if forecast[0][:2] == d.strftime('%d'):
        return now, forecast[1:]
    else:
        return now, forecast[:-1]

print(infoWeather('Tomsk'))
