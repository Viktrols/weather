import requests
import sys

from datetime import datetime
from geopy.geocoders import Nominatim
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import City, Record
from config import API_URL, API_TOKEN, DAYS_COUNT, CITIES, UNITS, EXCLUDE

geolocator = Nominatim(user_agent='weather')


def get_weather_for_city(lat, lon, city):
    '''Get weather forecast for city and add it to the database'''
    url = (f'{API_URL}?lat={lat}&lon={lon}&appid={API_TOKEN}&units={UNITS}&'
           f'cnt={DAYS_COUNT}&exclude={EXCLUDE}')
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError:
        status = response.status_code
        if status == 401:
            print('Invalid API key.')
        elif status == 404:
            print('Page not found.')
        sys.exit(1)

    weekly_forecast = response.json()['daily']
    for day in weekly_forecast:
        try:
            record = Record(
                date=datetime.utcfromtimestamp(day['dt']),
                temp=day['temp']['day'],
                pcp=get_pcp(day),
                clouds=day['clouds'],
                pressure=day['pressure'],
                humidity=day['humidity'],
                wind_speed=day['wind_speed'],
                city=City.query.filter_by(name=city).first().id
            )
            db.session.add(record)
            db.session.commit()
        except SQLAlchemyError as ex:
            print(f'SQLAlchemyError: {ex}')
            sys.exit(1)


def get_weather_for_cities(cities):
    '''Add cities from list to the database, get the latitude and longitude
       of these cities and get weather forecasts'''
    for city in cities:
        db.session.add(City(name=city))
        db.session.commit()
        location = geolocator.geocode(city)
        lat = location.latitude
        lon = location.longitude
        get_weather_for_city(lat, lon, city)


def get_pcp(day):
    '''Parsing precipitation from json'''
    rain = day.get('rain')
    snow = day.get('snow')
    if rain:
        return rain
    elif snow:
        return snow
    return 0


if __name__ == '__main__':
    get_weather_for_cities(CITIES)
