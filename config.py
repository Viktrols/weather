import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Constants for openweathermap
API_URL = 'https://api.openweathermap.org/data/2.5/onecall'
API_TOKEN = os.environ.get('API_KEY')
DAYS_COUNT = 7
UNITS = 'metric'
EXCLUDE = 'current,minutely,hourly,alerts'
CITIES = ['Kyiv', 'Odessa', 'Kharkiv', 'Sumi', 'Dnipro']

APISPEC_SPEC = {
    'APISPEC_SPEC':
        APISpec(title='Weather',
                version='v1',
                plugins=[MarshmallowPlugin()],
                openapi_version='2.0.0'
                ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
}
