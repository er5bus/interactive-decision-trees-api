from neomodel import StringProperty, StructuredNode, UniqueIdProperty, EmailProperty, DateTimeProperty
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class BaseStructuredNode(StructuredNode):
    __abstract_node__ = True

    load_relations = False


class UniqueIdMixin(object):
    """
    Add unique identifier to node
    """
    uid = UniqueIdProperty()


class TimestampMixin(object):
    """
    add created at and update at fields
    """
    created = DateTimeProperty(default_now=True)
    updated = DateTimeProperty(default_now=True)

    def pre_save(self):
        self.updated = datetime.now()


class UserMixin(object):
    """
    User auth values
    """
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


class RelationshipAccess(object):
    """
    A relationship descriptor that sets and returns values.
    """
    load_relations_attr = "load_relations"

    def __init__(self, rel=None, many=True):
        self.many = many
        self.rel = rel

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if hasattr(obj, self.load_relations_attr) and self.rel and getattr(obj, self.load_relations_attr):
            results = getattr(obj, self.rel).all()
            for node in results:
                setattr(node, self.load_relations_attr, True)
            return results if self.many else (results and results.pop())
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = list() if self.many else None
        return obj.__dict__.get(self.name)

    def __set__(self, obj, val):
        if not self.many and isinstance(val, list):
            val = val.pop()
        obj.__dict__[self.name] = val

