from flask import Blueprint
from ...tools import urls


# views
from .views.auth import UserRegisterView, UserLoginView, UserLogoutView

api = Blueprint('auth', __name__)


urls.add_url_rule(
    api,
    UserRegisterView,
    UserLoginView,
    UserLogoutView
)
