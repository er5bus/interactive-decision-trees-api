from flask import Blueprint
from ...tools import urls


api = Blueprint('nodes', __name__)


# views
from .views.content_node import ContentNodeCreateView, ContentNodeRetrieveUpdateDestroyView
from .views.logic_node import LogicNodeCreateView, LogicNodeRetrieveUpdateDestroyView
from .views.node import NodeRetrieveView
from .views.nodes import AllNodesRetriveView, TreeNodesListView
from .views.set_first_node import TreeFirstNodeSetView
from .views.set_last_node import TreeLastNodeSetView


urls.add_url_rule(
    api,
    ContentNodeCreateView,
    ContentNodeRetrieveUpdateDestroyView,
    LogicNodeCreateView,
    LogicNodeRetrieveUpdateDestroyView,
    NodeRetrieveView,
    AllNodesRetriveView,
    TreeNodesListView,
    TreeFirstNodeSetView,
    TreeLastNodeSetView
)
