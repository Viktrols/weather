from flask import Blueprint
from flask_restful import Api

from . import resources

weather_bp = Blueprint('weather_api', __name__)
weather_api = Api(weather_bp)

weather_api.add_resource(resources.Cities, '/cities/')
weather_api.add_resource(resources.Mean, '/mean/')
weather_api.add_resource(resources.Records, '/records/')
weather_api.add_resource(resources.MovingMean, '/moving_mean/')
