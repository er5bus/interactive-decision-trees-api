from .... import models, schemas
from ....tools.views import generics
from flask_jwt_extended import jwt_required


class TreeFirstNodeSetView(generics.ListCreateAPIView):
    route_path = "/tree/<string:tree_uid>/first/node/<string:node_uid>"
    route_name = "content_node_set_first_node"

    lookup_field_and_url_kwarg = { "tree": "tree_uid", "node": "node_uid" }

    schema_class = schemas.ContentNodeSchema
    decorators = [ jwt_required ]

    def filter_node(self, model_class=None, **kwargs):
        self.current_tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        if self.current_tree:
            return self.current_tree.load_tree_node(uid=kwargs.get("node"))
        return None

    def create(self, *args, **kwargs):
        content_node = self.get_node(**kwargs)
        content_node.is_first_node = True
        content_node.save()

        try:
            first_node = self.current_tree.first_node_rel.get()
            if first_node :
                first_node.is_first_node = False
                first_node.save()
        except:
            pass

        self.current_tree.first_node_rel.disconnect_all()
        self.current_tree.first_node_rel.connect(content_node)
        return self.serialize(content_node, many=False), 200


