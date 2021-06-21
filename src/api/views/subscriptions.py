from http import HTTPStatus
from json import JSONDecodeError

from flask import current_app, request
from flask.views import MethodView
from pydantic import ValidationError, parse_raw_as
from werkzeug.exceptions import BadRequest

from api.exceptions import LogicalException
from api.views.serializers.picture import EmailSerializer
from api.views.utils import jsonify_response, json_response


class SubscriptionListView(MethodView):

    def __init__(self):
        self._subscription_service = current_app.domain_services.subscription_service()

    def post(self):
        try:
            serialized = parse_raw_as(EmailSerializer, request.data)
        except JSONDecodeError as exception:
            raise BadRequest(exception.msg)
        except ValidationError as exception:
            return json_response(exception.json(), status_code=HTTPStatus.BAD_REQUEST)

        try:
            subscription_arn = self._subscription_service.subscribe(serialized.email)
        except LogicalException as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)

        return jsonify_response({"subscription_arn": subscription_arn})
