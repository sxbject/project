import requests
from config import Config

def get_weather(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': Config.OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed']
        }
    return None