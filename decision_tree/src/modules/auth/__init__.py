from flask import Blueprint


api = Blueprint('auth', __name__)
from . import urls
