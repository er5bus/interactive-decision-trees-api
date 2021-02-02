from flask import Blueprint
from ...tools import urls


api = Blueprint('trees', __name__)

# views
from .views.tags import TagsRetriveAllView, TagListCreateView, TagRetrieveUpdateDestroyView
from .views.trees import TreeListCreateView, TreeRetriveAllView, TreeRetrieveUpdateDestroyView
from .views.scores import ScoreRetriveView


urls.add_url_rule(
    api,
    TagsRetriveAllView,
    TagListCreateView,
    TagRetrieveUpdateDestroyView,
    TreeListCreateView,
    TreeRetriveAllView,
    TreeRetrieveUpdateDestroyView,
    ScoreRetriveView
)
