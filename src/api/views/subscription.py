from http import HTTPStatus

from flask import current_app
from flask.views import MethodView

from api.exceptions import LogicalException
from api.views.utils import jsonify_response


class SubscriptionDetailView(MethodView):

    def __init__(self):
        self._subscription_service = current_app.domain_services.subscription_service()

    def delete(self, subscription_arn: str):
        try:
            self._subscription_service.unsubscribe(subscription_arn)
        except LogicalException as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)
        return jsonify_response({}, status_code=HTTPStatus.NO_CONTENT)
