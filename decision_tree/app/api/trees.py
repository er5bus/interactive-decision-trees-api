from . import api
from .. import models, schemas
from ..views import utils, generics
from flask_jwt_extended import jwt_required, get_current_user


class TreeListCreateView(generics.ListCreateAPIView):

    route_path = "/trees"
    route_name = "tree_list_create"

    model_class = models.Tree
    schema_class = schemas.TreeSchema
    unique_fields = ("tree_name", )

    load_relationships = True

    decorators = [ jwt_required ]

    def perform_create(self, tree):
        tree.save()
        tree.owner_rel.connect(get_current_user())

        for tag in tree.tags or []:
            tree.tags_rel.connect(tag)

        for score in tree.scores or []:
            score.save()
            tree.scores_rel.connect(score)

    def filter_nodes(self, model_class=None, start=None, offset=None, **kwargs):
        user = get_current_user()
        return user.load_trees(start, abs(start - offset))

    def filter_unique_node(self, model_class=None, **kwargs):
        user = get_current_user()
        nodes = user.load_trees(**kwargs)
        if nodes:
            return nodes[0]
        return None


class TreeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/tree/<string:id>"
    route_name = "tree_retrieve_update_destroy"

    model_class = models.Tree
    schema_class = schemas.TreeSchema
    unique_fields = ("tree_name", )

    load_relationships = True

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"uid": "id"}

    def filter_node(self, model_class=None, **kwargs):
        user = get_current_user()
        nodes = user.load_trees(**kwargs)
        if nodes:
            return nodes[0]
        return None

    def perform_update(self, tree):
        super().perform_update(tree)
        for score in tree.scores_rel.all():
            if not tree.scores or score not in tree.scores:
                score.delete()

        tree.tags_rel.disconnect_all()
        for tag in tree.tags or []:
            tree.tags_rel.connect(tag)

        if tree.first_node:
            tree.first_node_rel.disconnect_all()
            tree.first_node_rel.connect(tree.first_node)

        for score in tree.scores or []:
            score.save()
            tree.scores_rel.connect(score)

    def perform_delete(self, tree):
        for score in tree.scores_rel.all():
            score.delete()
        super().perform_delete(tree)


class TreeRetriveAllView(generics.RetrieveAPIView):

    route_path = "/trees/all"
    route_name = "tree_retrieve_all"

    decorators = [ jwt_required ]

    model_class = models.Tree

    lookup_field_and_url_kwarg = { "uid": "tree_uid" }

    def filter_node(self, model_class=None, **kwargs):
        user = get_current_user()
        return user.load_trees(0, 500)

    def serialize(self, trees, many=False):
        items = []
        for tree in trees:
            if isinstance(tree.first_node, models.ContentNode):
                items.append({"value": tree.id, "label": tree.tree_name })
        return { "items": items }


utils.add_url_rule(api, TreeListCreateView, TreeRetriveAllView, TreeRetrieveUpdateDestroyView)
