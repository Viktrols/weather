from flask import Flask
from config import Config, APISPEC_SPEC
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(APISPEC_SPEC)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.api import weather_bp

app.register_blueprint(weather_bp)

docs = FlaskApiSpec(app)

from app.api import resources

docs.register(resources.Cities, blueprint='weather_api')
docs.register(resources.Mean, blueprint='weather_api')
docs.register(resources.Records, blueprint='weather_api')
docs.register(resources.MovingMean, blueprint='weather_api')
