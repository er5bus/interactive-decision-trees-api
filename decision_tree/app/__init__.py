from flask import Flask
from config import config
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from neomodel import config as neomodel_config


ma = Marshmallow()
jwt = JWTManager()
cors = CORS()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    neomodel_config.DATABASE_URL = config[config_name].NEOMODEL_DATABASE_URL
    neomodel_config.ENCRYPTED_CONNECTION = config[config_name].NEOMODEL_ENCRYPTED_CONNECTION
    neomodel_config.NEOMODEL_CYPHER_DEBUG = config[config_name].NEOMODEL_CYPHER_DEBUG

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
