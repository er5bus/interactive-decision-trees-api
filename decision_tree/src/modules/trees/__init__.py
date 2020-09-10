from flask import Blueprint


api = Blueprint('trees', __name__)
from . import urls
