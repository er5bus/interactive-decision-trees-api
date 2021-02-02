from manage import application
import traceback
import sys
from werkzeug.exceptions import HTTPException, InternalServerError, BadRequest


@application.errorhandler(BadRequest)
def handle_bad_request_exception(e):
    return {"code": e.name.lower().replace(" ", "-"), "message": e.name , "constraints": e.description}, e.code


@application.errorhandler(HTTPException)
def handle_exception(e):
    return {"code": e.name.lower().replace(" ", "-"), "message": e.name , "description": e.description}, e.code


@application.errorhandler(InternalServerError)
def handle_internal_exception(e):
    traceback.print_exc(file=sys.stdout)
    return {"code": "internal-error", "message": "something wrong happened", "description": e.description}, 500


if __name__ == "__main__":
    application.run()
