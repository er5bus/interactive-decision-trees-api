from . import auth
from werkzeug.exceptions import HTTPException


@auth.errorhandler(HTTPException)
def handle_exception(e):
    return {'error': e.name.lower().replace(' ', '-'), 'message': e.description}, e.code
