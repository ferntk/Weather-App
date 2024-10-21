import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from collections import defaultdict

load_dotenv()
api_key = os.getenv('API_KEY')


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int
    high: int
    low: int

    @property
    def titlecase_description(self):
        return self.description.title()


def get_lat_lon(city_name, state_code, country_code):
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={api_key}').json()
    if resp:
        data = resp[0]
        lat, lon = data.get('lat'), data.get('lon')
        return lat, lon
    return None, None


def get_current_weather(lat, lon):
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial').json()
    if 'weather' in resp:
        data = WeatherData(
            main=resp['weather'][0]['main'],
            description=resp['weather'][0]['description'],
            icon=resp['weather'][0]['icon'],
            temperature=int(resp['main']['temp']),
            high=int(resp['main']['temp_max']),
            low=int(resp['main']['temp_min'])
        )
        return data
    return None


def get_five_day_forecast(lat, lon):
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial').json()

    if 'list' in resp:
        daily_forecast = defaultdict(lambda: {
            'temps': [],
            'high': float('-inf'),
            'low': float('inf'),
            'main': resp['list'][0]['weather'][0]['main'],
            'description': resp['list'][0]['weather'][0]['description'],
            'icon': resp['list'][0]['weather'][0]['icon']
        })

        for entry in resp['list']:
            date = entry['dt_txt'].split(" ")[0]
            temp = entry['main']['temp']
            daily_forecast[date]['temps'].append(temp)
            daily_forecast[date]['high'] = max(daily_forecast[date]['high'], entry['main']['temp_max'])
            daily_forecast[date]['low'] = min(daily_forecast[date]['low'], entry['main']['temp_min'])

        forecast_data = []
        for date, data in daily_forecast.items():
            average_temp = sum(data['temps']) / len(data['temps'])
            forecast_data.append({
                'date': date,
                'main': data['main'],
                'description': data['description'],
                'icon': data['icon'],
                'temperature': round(average_temp),
                'high': round(data['high']),
                'low': round(data['low']),
            })
        return forecast_data

    return None


def main(city_name, state_code, country_code):
    lat, lon = get_lat_lon(city_name, state_code, country_code)
    if lat is not None and lon is not None:
        current_weather = get_current_weather(lat, lon)
        weekly_forecast = get_five_day_forecast(lat, lon)
        return current_weather, weekly_forecast
    return None, None
