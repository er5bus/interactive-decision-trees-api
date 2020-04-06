from app import create_app
import os


application = create_app(os.getenv('FLASK_CONFIG', 'default'))


@application.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    application.run(debug=True)
