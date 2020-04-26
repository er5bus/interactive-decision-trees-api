from . import api
from .. import models, schemas
from ..views import utils, generics
from flask_jwt_extended import jwt_required, get_current_user


class TagListCreateView(generics.ListCreateAPIView):

    route_path = "/tags"
    route_name = "tag_list_create"

    model_class = models.Tag
    schema_class = schemas.TagSchema
    unique_fields = ("name", )

    load_relationships = True

    decorators = [ jwt_required ]

    def perform_create(self, tag):
        tag.save()
        tag.owner_rel.connect(get_current_user())

    def filter_nodes(self, model_class=None, start=None, offset=None, **kwargs):
        user = get_current_user()
        return user.load_tags(start, abs(start - offset))

    def filter_unique_node(self, model_class=None, **kwargs):
        user = get_current_user()
        nodes = user.load_tags(**kwargs)
        if nodes:
            return nodes[0]
        return None


class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/tag/<string:id>"
    route_name = "tag_retrieve_update_destroy"

    model_class = models.Tag
    schema_class = schemas.TagSchema
    unique_fields = ("name", )

    load_relationships = True

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"uid": "id"}

    def filter_node(self, model_class=None, **kwargs):
        user = get_current_user()
        nodes = user.load_tags(**kwargs)
        if nodes:
            return nodes[0]
        return None


class TagsRetriveView(generics.RetrieveAPIView):

    route_path = "/tags/all"
    route_name = "tags_retrieve"

    decorators = [ jwt_required ]

    def retrieve(self, *args, **kwargs):
        user = get_current_user()
        return { "items": [ {"value": tag.id, "label": tag.name, "description": tag.description } for tag in user.load_tags() ] }, 200


utils.add_url_rule(api, TagListCreateView, TagRetrieveUpdateDestroyView, TagsRetriveView)
