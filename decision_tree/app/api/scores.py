from . import api
from .. import models, schemas
from ..views import utils, generics
from flask import abort
from flask_jwt_extended import jwt_required


class ScoreRetriveView(generics.RetrieveAPIView):

    route_path = "/tree/<string:id>/all/scores"
    route_name = "tree_retrieve_scores"

    decorators = [ jwt_required ]

    def retrieve(self, *args, **kwargs):
        tree = models.Tree.nodes.filter(uid__exact=kwargs.get("id")).get_or_none()
        if tree is None:
            abort(404)
        print(tree.fetch_all_tree_scores())
        return { "items": [ {"value": score.id, "label": score.name, "description": score.description } for score in tree.fetch_all_tree_scores() ] }, 200


utils.add_url_rule(api, ScoreRetriveView)
