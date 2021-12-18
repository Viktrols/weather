from sqlalchemy import (Column,
                        ForeignKey,
                        Integer,
                        String,
                        )
from sqlalchemy.sql.sqltypes import DateTime, Float

from app import db


class City(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    records = db.relationship('Record', backref='city_weather', lazy='dynamic')


class Record(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    temp = Column(Float, nullable=False)
    pcp = Column(Float, nullable=False)
    clouds = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    city = Column(Integer, ForeignKey('city.id'))
