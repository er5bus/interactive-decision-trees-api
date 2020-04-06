from . import api
from .. import models, schemas
from views import utils, generics
from flask_jwt_extended import jwt_required, get_current_user


class TreeListCreateView(generics.ListCreateAPIView):

    route_path = "/trees"
    route_name = "tree_list_create"

    model_class = models.Tree
    schema_class = schemas.TreeSchema
    unique_fields = ("tree_name", )

    load_relationship = { "scores": True, "owner": True }

    decorators = [ jwt_required ]

    def perform_create(self, instance, relationship_instances):
        relationship_instances["owner"] = get_current_user()
        super().perform_create(instance, relationship_instances)


class TreeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/tree/<string:id>"
    route_name = "tree_retrieve_update_destroy"

    model_class = models.Tree
    schema_class = schemas.TreeSchema
    unique_fields = ("tree_name", )

    load_relationship = { "scores": True, "owner": True }

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"uid": "id"}


utils.add_url_rule(api, TreeListCreateView, TreeRetrieveUpdateDestroyView)
