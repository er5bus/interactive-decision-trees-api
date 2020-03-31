from flask import Response, request, abort
from marshmallow.exceptions import ValidationError
from copy import deepcopy
from flask_jwt_extended import jwt_required
from neomodel import db


class BaseMethodMixin:
    """
    Base API methods
    """

    route_path = None
    route_name = None

    model_class = None
    schema_class = None

    # lookup_field as the key and lookup_url_kwarg as the value
    lookup_field_and_url_kwarg = dict()

    unique_fields = tuple()

    methods = tuple()

    jwt_required = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.jwt_required:
            self.decorators += (jwt_required, )

    def filter_nodes(self, **kwargs):
        with db.read_transaction:
            nodes = self.model.nodes
            if kwargs:
                filter_kwargs = {}
                for lookup_field, lookup_url_kwarg in self.lookup_field_and_url_kwarg.items():
                    filter_kwargs["{0}__exact".format(lookup_field)] = kwargs.get(lookup_url_kwarg, None)
                return nodes.filter(**filter_kwargs)
            return nodes

    def get_node(self, **kwargs):
        instance = self.filter_nodes(**kwargs)
        if instance is None:
            abort(404)
        return instance

    def paginate_nodes(self, **kwargs):
        page = request.args.get('page', type=int, default=1)
        item_per_page = request.args.get('item_per_page', type=int, default=10)
        offset = page * item_per_page
        return self.filter_nodes(**kwargs)[(offset - item_per_page):offset]

    def serialize(self, data = [], many=False):
        serializer = self.schema_class(many=many, unknown='EXCLUDE')
        return serializer.dump(data)

    def validate_unique(self, data = [], many=True):
        for unique_field in self.unique_fields:
            unique_node = self.filter_nodes(**{ unique_field: getattr(new_instance, unique_field) })
            if (unique_object is not None and instance is None) or (unique_object is not None and unique_object.id != instance.id):
                errors[unique_field] = "{} already exist.".format(unique_field)
        raise ValidationError(errors)

    def deserialize(self, data = [], params = [], instance=None, partial=False):
        serializer = self.schema_class()
        try:
            return serializer.load(data, instance=instance, unknown='INCLUDE', partial=partial)
        except ValidationError as err:
            self.raise_exception(err)
    def raise_exception(self, errors):
        abort(400, errors.messages)


class ListMixin(BaseMethodMixin):
    """
    List model objects.
    """

    def list (self, *args, **kwargs):
        paginator = self.paginate_nodes(**kwargs)
        return dict(items=self.serialize(paginator.items, True), has_more=paginator.has_next, next=next_url, previous=previous_url), 200


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
        instance = self.deserialize(request.json)
        self.perform_create(instance)
        return self.serialize(instance), 201

    def perform_create(self, instance):
        with db.write_transaction:
            instance.save()


class UpdateMixin(BaseMethodMixin):
    """
    Update model instance
    """
    def update (self, *args, **kwargs):
        with db.session.no_autoflush:
            instance = self.get_node(**kwargs)
            old_instance = deepcopy(instance)
            instance_updated = self.deserialize(request.json, instance=instance ,partial=False)
            self.perform_update(old_instance, instance_updated)

        return self.serialize(instance_updated), 200

    def partial_update (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        old_instance = deepcopy(instance)
        instance_updated = self.deserialize(request.json, instance=instance, partial=True)
        self.perform_update(old_instance, instance_updated)

        return self.serialize(instance_updated), 200


    def perform_update(self, old_instance, instance_updated):
        with db.write_transaction:
            instance_updated.save()


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
    access_control_allowed_headers = 'Content-Type, Authorization, X-Requested-With'
    access_control_max_age = 120
    access_control_allowed_credentials = False
    access_control_exposed_headers = '*'

    def cors_preflight (self, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Headers' : self.access_control_allowed_headers,
            'Access-Control-Allow-Methods': self.methods,
            'Access-Control-Max-Age': self.access_control_max_age,
            'Access-Control-Allow-Credentials': self.access_control_allowed_credentials,
            'Access-Control-Expose-Headers': self.access_control_exposed_headers,
            'Vary': 'Origin'  # in case of server cache the response and the origin is not a wild card
        }
        return Response(status=204, headers=headers)
