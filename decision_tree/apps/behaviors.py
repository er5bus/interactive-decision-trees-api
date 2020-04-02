from neomodel import StringProperty, UniqueIdProperty, EmailProperty, DateTimeProperty
from werkzeug.security import generate_password_hash, check_password_hash


class UniqueIdMixin(object):
    uid = UniqueIdProperty()


class TimestampMixin(object):
    created = DateTimeProperty(default_now=True)
    updated = DateTimeProperty(default_now=True)


class UserMixin(object):
    email = EmailProperty(unique_index=True)
    hashed_password = StringProperty()

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, plain_password):
        self.hashed_password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.hashed_password, plain_password)
