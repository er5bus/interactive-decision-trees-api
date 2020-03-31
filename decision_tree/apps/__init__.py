from flask import Flask
from config import config
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from neomodel import config as neomodel_config


ma = Marshmallow()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    ma.init_app(app)
    jwt.init_app(app)

    neomodel_config.DATABASE_URL = config[config_name].DATABASE_URL

    return app
