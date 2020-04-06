from . import api
from werkzeug.exceptions import HTTPException


@api.errorhandler(HTTPException)
def handle_exception(e):
    return {'error': e.name.lower().replace(' ', '-'), 'message': e.description}, e.code
