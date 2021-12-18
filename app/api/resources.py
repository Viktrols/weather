from flask import jsonify, make_response, request
from flask_apispec import doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from sqlalchemy.sql import func

from app.models import City, Record
from app import db


class Cities(MethodResource, Resource):
    @doc(description='Return list of cities from the Database',
         tags=['Cities']
         )
    def get(self):
        all_cities = db.session.query(City.name).all()
        cities_names = [city[0] for city in all_cities]
        return make_response(jsonify(cities=cities_names), 200)


class Mean(Resource, MethodResource):
    @doc(description='Return the average value of the selected parameter'
                     'for the selected city',
         tags=['Mean'],
         params={
             'city': {
                 'description': 'The name of the city fo'
                                'which the calculation will be made',
                 'in': 'query',
                 'type': 'str',
                 'required': True},
             'value_type': {
                 'description': 'Value: temp, pcp, clouds, pressure,'
                                'humidity or wind_speed',
                 'in': 'query',
                 'type': 'str',
                 'required': True}
         }
         )
    def get(self):
        city_name = request.args.get('city')
        value_type = request.args.get('value_type')
        if not city_name or not value_type:
            return jsonify(message='Make sure to enter'
                                   'all required parameters.')
        try:
            city = City.query.filter_by(name=city_name).first()
            column = getattr(Record, value_type)
            average = db.session.query(func.avg(column)).where(
                                       Record.city == city.id).all()
            return make_response(jsonify(result=average[0][0]), 200)
        except AttributeError:
            return jsonify(message='Parameters are invalid.')


class Records(Resource, MethodResource):
    @doc(description='Return a list of weather forecasts'
                     'for the selected city and period',
         tags=['Records'],
         params={
             'city': {
                 'description': 'Name of the city for which the'
                                'weather forecasts will return',
                 'in': 'query',
                 'type': 'str',
                 'required': True},
             'start_dt': {
                 'description': 'Start date',
                 'in': 'query',
                 'type': 'date',
                 'required': True},
             'end_dt': {
                 'description': 'End date',
                 'in': 'query',
                 'type': 'date',
                 'required': True}
         }
         )
    def get(self):
        city_name = request.args.get('city')
        start_dt = request.args.get('start_dt')
        end_dt = request.args.get('end_dt')
        if not city_name or not start_dt or not end_dt:
            return jsonify(message='Make sure to enter'
                                   'all required parameters.')

        try:
            city = City.query.filter_by(name=city_name).first()
            records = Record.query.filter(Record.city == city.id,
                                          Record.date >= start_dt,
                                          Record.date <= end_dt).all()
            result = []
            for record in records:
                record_dict = dict({
                    'date': record.date,
                    'temp': record.temp,
                    'pcp': record.pcp,
                    'clouds': record.clouds,
                    'pressure': record.pressure,
                    'humidity': record.humidity,
                    'wind_speed': record.wind_speed,
                })
                result.append(record_dict)
            return make_response(jsonify(all_records=result), 200)
        except AttributeError:
            return jsonify(message='Parameters are invalid.')


class MovingMean(Resource, MethodResource):
    @doc(description='Return the moving average value of the selected'
                     'parameter for the selected city for all days',
         tags=['Moving Mean'],
         params={
             'city': {
                 'description': 'The name of the city for which'
                                'the calculation will be made',
                 'in': 'query',
                 'type': 'str',
                 'required': True},
             'value_type': {
                 'description': 'Value: temp, pcp, clouds, pressure,'
                                'humidity or wind_speed',
                 'in': 'query',
                 'type': 'str',
                 'required': True}
         }
         )
    def get(self):
        city_name = request.args.get('city')
        value_type = request.args.get('value_type')
        if not city_name or not value_type:
            return jsonify(message='Make sure to enter'
                                   'all required parameters.')
        try:
            city = City.query.filter_by(name=city_name).first()
            column = getattr(Record, value_type)
            records = db.session.query(column, Record.date).where(
                                       Record.city == city.id).all()
            result = []
            for i, record in enumerate(records):
                date = record[1].strftime('%d/%m/%Y')
                value = record[0]
                if i == 0:
                    result.append({date: None})
                else:
                    all_values = [value]
                    for record in records[:i]:
                        all_values.append(record[0])
                    moving_avg = (sum(all_values)) / len(all_values)
                    result.append({date: moving_avg})
            return make_response(jsonify(result=result), 200)
        except AttributeError:
            return jsonify(message='Parameters are invalid.')
