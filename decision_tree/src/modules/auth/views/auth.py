from .... import models, schemas, jwt
from ....tools.views import generics
from flask import request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt, get_jti, jwt_required


blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@jwt.user_loader_callback_loader
def user_loader_callback_loader(jwt_identity):
    return models.User.nodes.filter(uid__exact=jwt_identity).get_or_none()


class UserRegisterView(generics.CreateAPIView, generics.OptionsAPIView):

    route_path = "/auth/register"
    route_name = "user_register"

    model_class = models.User
    schema_class = schemas.UserSchema
    unique_fields = ("email", )

    access_token = None

    def create (self, *args, **kwargs):
        (response, code) = super().create(self, *args, **kwargs)
        return {**response, "access_token": self.access_token }, code

    def perform_create(self, instance):
        super().perform_create(instance)
        self.access_token = create_access_token(identity=instance.uid)


class UserLoginView(generics.CreateAPIView, generics.OptionsAPIView):
    route_path = "/auth/login"
    route_name = "user_login"

    def post(self, *args, **kwargs):
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        current_user = models.User.nodes.get_or_none(email__exact=email) if password or email else None
        if current_user is not None and current_user.check_password(password):
            data = schemas.UserSchema(many=False).dump(current_user)
            return {**data ,"access_token": create_access_token(identity=current_user.uid)}, 200
        return abort(400, {"Oops": "Invalid email or password."})


class UserLogoutView(generics.CreateAPIView):

    route_path = "/auth/logout"
    route_name = "user_logout"

    decorators = [jwt_required]

    def post(self, *args, **kwargs):
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200
