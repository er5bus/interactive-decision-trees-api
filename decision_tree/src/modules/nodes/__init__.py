from flask import Blueprint


api = Blueprint('nodes', __name__)
from . import urls
