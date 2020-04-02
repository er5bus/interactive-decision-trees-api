from . import models, ma
from marshmallow import validates_schema, ValidationError, INCLUDE, EXCLUDE
from marshmallow.validate import Length, Range, ContainsOnly


class UniqueIdMixin(object):
    uid = ma.String(dump_only=True)


class TimestampMixin(object):
    created = ma.DateTime()
    updated = ma.DateTime()


class UserSchema(ma.Schema, UniqueIdMixin, TimestampMixin):
    fullname = ma.String(max_length=200, required=True, validate=Length(max=200, min=1))
    email = ma.String(max_length=128, required=True, validate=Length(max=128, min=1))
    password = ma.String(max_length=128, required=False, load_only=True)

    class Meta:
        model = models.User
