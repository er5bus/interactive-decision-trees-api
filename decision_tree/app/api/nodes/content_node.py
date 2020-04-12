from .. import api
from ... import models, schemas
from views import utils, generics
from flask_jwt_extended import jwt_required, get_current_user


class ContentNodeCreateView(generics.CreateAPIView):

    route_path = "/tree/<string:tree_uid>/node/content"
    route_name = "content_node_create"

    schema_class = schemas.ContentNodeSchema

    lookup_field_and_url_kwarg = {"uid": "tree_uid"}

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.current_tree = self.get_node(model_class=models.Tree, **kwargs)
        return super().create(*args, **kwargs)

    def perform_create(self, content_node_instance):
        content_node_instance.save()
        for action in content_node_instance.actions:
            action.save()
            if action.point_to and action.point_to.id:
                action.point_to_rel.connect(action.point_to)
            for action_value in action.values or []:
                action_value.save()
                if action_value.score:
                    action_value.score_rel.connect(action_value.score)
                action.values_rel.connect(action_value)
            content_node_instance.actions_rel.connect(action)
        content_node_instance.tree_rel.connect(self.current_tree)
        self.current_tree.tree_nodes_rel.connect(content_node_instance)


class ContentNodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/tree/<string:tree_uid>/node/content/<string:node_uid>"
    route_name = "content_node_retrieve_update_destroy"

    model_class = models.ContentNode
    schema_class = schemas.ContentNodeSchema

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"tree": "tree_uid" , "node": "node_uid"}

    def filter_node(self, model_class=None, **kwargs):
        tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        content_node = tree.load_tree_node(kwargs.get("node"))
        content_node.load_relations = True
        return content_node

    def perform_relation_delete(self, content_node_instance):
        # delete actions
        for action in content_node_instance.actions_rel.all():
            for action_value in action.values_rel.all():
                if action_value not in [ action.values or [] for action in content_node_instance.actions ]:
                    action_value.delete()
            if content_node_instance.actions or action not in content_node_instance.actions:
                action.delete()


    def perform_update(self, content_node_instance):
        content_node_instance.save()
        self.perform_relation_delete(content_node_instance)
        for action in content_node_instance.actions:
            action.save()
            if action.point_to and action.point_to.id:
                action.point_to_rel.connect(action.point_to)
            else:
                action.point_to_rel.disconnect_all()
            for action_value in action.values or []:
                action_value.save()
                if action_value.score:
                    action_value.score_rel.connect(action_value.score)
                action.values_rel.connect(action_value)
            content_node_instance.actions_rel.connect(action)

    def perform_delete(self, content_node_instance):
        self.perform_relation_delete(content_node_instance)
        super().perform_delete(content_node_instance)


utils.add_url_rule(api, ContentNodeCreateView, ContentNodeRetrieveUpdateDestroyView)
