from flask import Blueprint

from api.views.healthcheck import HealthCheckView
from api.views.metadata import PictureMetadataDetailView, PictureMetadataRandomView
from api.views.pictures import PictureListView
from api.views.picture import PictureDetailView
from api.views.subscription import SubscriptionDetailView
from api.views.subscriptions import SubscriptionListView

bp = Blueprint("storage", __name__)

bp.add_url_rule(
    "pictures",
    view_func=PictureListView.as_view("picture-list"),
    methods=["POST", "GET"],
)
bp.add_url_rule(
    "pictures/metadata",
    view_func=PictureMetadataRandomView.as_view("picture-random-metadata"),
    methods=["GET"],
)
bp.add_url_rule(
    "pictures/<picture_name>",
    view_func=PictureDetailView.as_view("picture-detail"),
    methods=["GET", "DELETE", "PATCH"],
)
bp.add_url_rule(
    "pictures/<picture_name>/metadata",
    view_func=PictureMetadataDetailView.as_view("picture-metadata-detail"),
    methods=["GET"],
)
bp.add_url_rule(
    "subscriptions",
    view_func=SubscriptionListView.as_view("subscription-list"),
    methods=["POST"],
)
bp.add_url_rule(
    "subscriptions/<subscription_arn>",
    view_func=SubscriptionDetailView.as_view("subscription-detail"),
    methods=["DELETE"],
)

bp.add_url_rule(
    "healthcheck",
    view_func=HealthCheckView.as_view("healthcheck"),
    methods=["GET"],
)
