from .. import models, ma
from ._behaviors import BaseSchema, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length


class UserSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__ = models.User

    full_name = ma.String(max_length=200, required=True, validate=Length(max=200, min=1))
    email = ma.String(max_length=128, required=True, validate=Length(max=128, min=1))
    password = ma.String(max_length=128, required=False, load_only=True)
