from app import create_app
from werkzeug.exceptions import HTTPException
import os


application = create_app(os.getenv('FLASK_CONFIG', 'default'))


@application.errorhandler(HTTPException)
def handle_exception(e):
    return {'error': e.name.lower().replace(' ', '-'), 'code': e.code, 'message': e.description}, e.code


@application.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    application.run(debug=True)
