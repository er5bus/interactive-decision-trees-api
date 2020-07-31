from flask import request, abort, jsonify
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_current_user
from neomodel import db, Q
from collections import Iterable


class BaseMethodMixin:
    """
    Base API methods
    """

    route_path = None
    route_name = None

    model_class = None
    schema_class = None

    load_relationships = False

    # lookup_field as the key and lookup_url_kwarg as the value
    lookup_field_and_url_kwarg = dict()

    unique_fields = tuple()

    methods = set()

    item_per_page = 10

    def filter_node(self, model_class=None, **kwargs):
        nodes = self.model_class.nodes if not model_class else model_class.nodes
        if kwargs:
            filter_kwargs = dict()
            for lookup_field, value in kwargs.items():
                filter_kwargs["{0}__exact".format(lookup_field)] = value
            node = nodes.filter(**filter_kwargs).get_or_none()
            if node:
                node.load_relations = self.load_relationships
            return node
        return None

    def filter_nodes(self, model_class=None, start=None, offset=None, **kwargs):
        nodes = self.model_class.nodes if not model_class else model_class.nodes
        if kwargs:
            filter_kwargs = dict()
            for lookup_field, value in kwargs.items():
                filter_kwargs["{0}__exact".format(lookup_field)] = value
            nodes = nodes.filter(**filter_kwargs)
        nodes = nodes[start:offset]
        for node in nodes:
            node.load_relations = self.load_relationships
        return nodes

    def filter_unique_node(self, model_class=None, **kwargs):
        return self.filter_node(model_class=model_class, **kwargs)

    def get_node(self, model_class=None, **kwargs):
        filter_kwargs = {}
        for lookup_field, lookup_url_kwarg in self.lookup_field_and_url_kwarg.items():
            filter_kwargs[lookup_field] = kwargs.get(lookup_url_kwarg, None)
        with db.read_transaction:
            instance = self.filter_node(model_class=model_class, **filter_kwargs)
        if instance is None:
            abort(404)
        return instance

    def paginate_nodes(self, model_class=None, **kwargs):
        page = request.args.get("page", type=int, default=1)
        item_per_page = request.args.get("item_per_page", type=int, default=self.item_per_page)
        offset = (page * item_per_page)
        start = (offset - item_per_page)
        with db.read_transaction:
            items = self.filter_nodes(model_class=model_class, start=start, offset=offset, **kwargs)
        return items, len(items) == item_per_page, page

    def serialize(self, data = [], many=False, schema_class=None):
        serializer = self.schema_class(many=many) if not schema_class else schema_class(many=many)
        return serializer.dump(data)

    def validate_unique(self, instance, current_node = None):
        errors = {}
        for unique_field in self.unique_fields:
            unique_node = self.filter_unique_node(**{ unique_field: getattr(instance, unique_field) })
            if (unique_node and not current_node) or (unique_node and current_node and int(unique_node.id) != int(current_node.id)):
                errors[unique_field] = "This {} is already exist.".format(unique_node.__class__.__name__)
        if errors:
            raise ValidationError(errors)

    def deserialize(self, data = [], node = None, partial=False, schema_class=None):
        try:
            serializer = self.schema_class(unknown=EXCLUDE) if not schema_class else schema_class(unknown=EXCLUDE)
            if node:
                node.load_relations = False
            serializer.context = dict(instance=node)
            instance = serializer.load(data, partial=partial)
            self.validate_unique(instance, node)
            return instance
        except ValidationError as err:
            self.raise_exception(err)

    def raise_exception(self, errors):
        abort(400, errors.messages)
