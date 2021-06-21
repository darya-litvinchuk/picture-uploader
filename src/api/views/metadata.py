from http import HTTPStatus

from flask import current_app
from flask.views import MethodView

from api.exceptions import LogicalException, NotFoundException
from api.views.utils import jsonify_response


class PictureMetadataDetailView(MethodView):

    def __init__(self):
        self._storage_service = current_app.domain_services.storage_service()

    def get(self, picture_name: str):
        try:
            metadata = self._storage_service.picture_metadata(picture_name)
        except (NotFoundException, LogicalException) as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)
        return jsonify_response(metadata)


class PictureMetadataRandomView(MethodView):

    def __init__(self):
        self._storage_service = current_app.domain_services.storage_service()

    def get(self):
        try:
            metadata = self._storage_service.random_metadata()
        except (NotFoundException, LogicalException) as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)
        return jsonify_response(metadata)
