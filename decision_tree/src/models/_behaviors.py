from neomodel import StringProperty, StructuredNode, UniqueIdProperty, EmailProperty, DateTimeProperty
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class BaseStructuredNode(StructuredNode):
    __abstract_node__ = True
    load_relations = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cypher_query = CypherQueryBuilder(self.cypher)


class CypherQueryBuilder(object):

    def __init__(self, cypher_func):
        self.cypher_query = ""
        self.cypher = cypher_func

    def cypher_query_builder(self, alias = "a"):
        self.cypher_query = "MATCH ({alias}) WHERE id({alias})".format(alias=alias) + "={self} "
        return self

    def return_alias(self, alias, attr=None):
        self.cypher_query += " RETURN {0}".format(alias)
        if attr:
            self.cypher_query += ".{0}".format(attr)
        return self

    def match(self, from_alias, relationship, to_alias):
        self.cypher_query += " MATCH ({0})-[:{1}]->({2})".format(from_alias, relationship, to_alias)
        return self

    def and_where(self, alias, **kwargs):
        self.cypher_query += self.where(alias, "AND", **kwargs)
        return self

    def or_where(self, alias, **kwargs):
        self.cypher_query += self.where(alias, "OR", **kwargs)
        return self

    def where(self, alias, operator, **kwargs):
        cypher_query = ""
        for attr, value in kwargs.items():
            cypher_query += operator if cypher_query else "WHERE "
            cypher_query += " {alias}.{attr} = '{value}'".format(alias=alias, attr=attr, value=value)
        return cypher_query

    def paginate(self, skip, limit):
        if skip is not None and limit is not None:
            self.cypher_query += " SKIP {skip} LIMIT {limit}".format(skip=skip, limit=limit)
        return self

    def get_one_or_none(self, func):
        try:
            results, columns = self.cypher(self.cypher_query)
            return func(results[0][0])
        except IndexError:
            return None

    def get_all(self, func):
        results, columns = self.cypher(self.cypher_query)
        items = []
        for row in results:
            item = func(row[0])
            item.load_relations = True
            items.append(item)
        return items


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


class LazyLoadingRelationship(object):
    """
    A relationship descriptor that sets and returns values.
    """

    load_relations_attr = "load_relations"

    def __init__(self, relationship=None, many=True, order_by='?'):
        self.many = many
        self.rel = relationship
        self.order_by = order_by

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if hasattr(obj, self.load_relations_attr) and self.rel and getattr(obj, self.load_relations_attr):
            results = getattr(obj, self.rel).order_by(self.order_by).all()
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

