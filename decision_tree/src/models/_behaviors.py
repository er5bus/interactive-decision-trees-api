from neomodel import StringProperty, StructuredNode, UniqueIdProperty, EmailProperty, DateTimeProperty
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ._cypher_query import CypherQueryBuilder


class BaseStructuredNode(StructuredNode):
    __abstract_node__ = True
    load_relations = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cypher_query = CypherQueryBuilder(self.cypher)


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

