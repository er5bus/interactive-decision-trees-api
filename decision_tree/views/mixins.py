from flask import Response, request, abort
from marshmallow.exceptions import ValidationError
from copy import deepcopy
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

    load_relationship = dict()

    # lookup_field as the key and lookup_url_kwarg as the value
    lookup_field_and_url_kwarg = dict()

    unique_fields = tuple()

    methods = set()

    def filter_nodes(self, **kwargs):
        with db.read_transaction:
            nodes = self.model_class.nodes
            for relationship_attr, value in self.load_relationship.items():
                nodes = nodes.has(**{relationship_attr: value})
            if kwargs:
                filter_kwargs = dict()
                for lookup_field, value in kwargs.items():
                    filter_kwargs["{0}__exact".format(lookup_field)] = value
                return nodes.filter(**filter_kwargs).get_or_none()
        return nodes

    def get_node(self, **kwargs):
        filter_kwargs = {}
        for lookup_field, lookup_url_kwarg in self.lookup_field_and_url_kwarg.items():
            filter_kwargs[lookup_field] = kwargs.get(lookup_url_kwarg, None)
        instance = self.filter_nodes(**filter_kwargs)
        if instance is None:
            abort(404)
        return instance

    def paginate_nodes(self, **kwargs):
        page = request.args.get("page", type=int, default=1)
        item_per_page = request.args.get("item_per_page", type=int, default=10)
        offset = page * item_per_page
        items = self.filter_nodes(**kwargs)[(offset - item_per_page):offset]
        return items, len(items) == item_per_page

    def serialize(self, data = [], many=False):
        serializer = self.schema_class(many=many, unknown="EXCLUDE")
        return serializer.dump(data)

    def validate_unique(self, instance, current_node = None):
        errors = {}
        for unique_field in self.unique_fields:
            unique_node = self.filter_nodes(**{ unique_field: getattr(instance, unique_field) })
            if (unique_node and not current_node) or (unique_node and current_node and int(unique_node.id) != int(current_node.id)):
                errors["Oops!"] = "{} field already exist.".format(unique_field)
        if errors:
            raise ValidationError(errors)

    def deserialize(self, data = [], node = None, partial=False):
        try:
            serializer = self.schema_class()
            serializer.context = dict(instance=node)
            instance, relationship_instances = serializer.load(data, unknown="EXCLUDE", partial=partial)
            self.validate_unique(instance, node)
            return instance, relationship_instances
        except ValidationError as err:
            self.raise_exception(err)

    def raise_exception(self, errors):
        abort(400, errors.messages)


class ListMixin(BaseMethodMixin):
    """
    List model objects.
    """

    def list (self, *args, **kwargs):
        (items, has_next) = self.paginate_nodes(**kwargs)
        return dict(items=self.serialize(items, True), has_more=has_next), 200


class RetrieveMixin(BaseMethodMixin):
    """
    Retrieve a model instance
    """

    def retrieve (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        return self.serialize(instance), 200


class CreateMixin(BaseMethodMixin):
    """
    Create a model instance
    """
    def create (self, *args, **kwargs):
        instance, relationship_instances = self.deserialize(request.json)
        with db.transaction:
            self.perform_create(instance, relationship_instances)
        return self.serialize(instance), 201

    def perform_create(self, instance, relationship_instances):
        instance.save()
        for relationship_attr, relationship_instance in relationship_instances.items():
            instance_attr = getattr(instance, relationship_attr)
            if isinstance(relationship_instance, Iterable):
                for relation in relationship_instance:
                    relation.save()
                    instance_attr.connect(relation)
            else:
                relationship_instance.save()
                instance_attr.connect(relationship_instance)


class UpdateMixin(BaseMethodMixin):
    """
    Update model instance
    """
    def update (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        instance_updated, relationship_instances = self.deserialize(request.json, deepcopy(instance), partial=False)
        with db.transaction:
            self.perform_update(instance_updated, relationship_instances)

        return self.serialize(instance_updated), 200

    def partial_update (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        instance_updated, relationship_instances = self.deserialize(request.json ,partial=True)
        with db.transaction:
            self.perform_update(instance, relationship_instances)

        return self.serialize(instance_updated), 200


    def perform_update(self, instance, relationship_instances):
        instance.save()
        for relationship_attr, relationship_instance in relationship_instances.items():
            instance_attr = getattr(instance, relationship_attr)
            if isinstance(relationship_instance, Iterable):
                for relation in relationship_instance:
                    print(relation)
                    relation.save()
                    instance_attr.connect(relation)
            else:
                relationship_instance.save()
                instance_attr.connect(relationship_instance)


class DeleteMinxin(BaseMethodMixin):
    """
    Delete model instance
    """
    def destroy (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        self.perform_delete(instance)

        return Response(status=204)

    def perform_delete(self, instance):
        with db.write_transaction:
            instance.delete()


class OptionsMixin:
    """
    CORS Preflight Mixin
    """
    access_control_allowed_headers = "Content-Type, Authorization, X-Requested-With"
    access_control_max_age = 120
    access_control_allowed_credentials = False
    access_control_exposed_headers = "*"

    def cors_preflight (self, *args, **kwargs):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers" : self.access_control_allowed_headers,
            "Access-Control-Allow-Methods": tuple(self.methods),
            "Access-Control-Max-Age": self.access_control_max_age,
            "Access-Control-Allow-Credentials": self.access_control_allowed_credentials,
            "Access-Control-Expose-Headers": self.access_control_exposed_headers,
            "Vary": "Origin"  # in case of server cache the response and the origin is not a wild card
        }
        return Response(status=204, headers=headers)
