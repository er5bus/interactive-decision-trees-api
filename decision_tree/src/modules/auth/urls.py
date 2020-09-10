from . import api
from ...tools import urls

# views
from .views.auth import UserRegisterView, UserLoginView, UserLogoutView


urls.add_url_rule(
    api, 
    UserRegisterView, 
    UserLoginView, 
    UserLogoutView
)
