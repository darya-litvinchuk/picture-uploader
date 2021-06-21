from http import HTTPStatus
from io import BytesIO

from flask import current_app, send_file
from flask.views import MethodView

from api.exceptions import LogicalException, NotFoundException
from api.views.utils import jsonify_response


class PictureDetailView(MethodView):

    def __init__(self):
        self._storage_service = current_app.domain_services.storage_service()

    def get(self, picture_name: str):
        try:
            file_dto = self._storage_service.download(picture_name)
        except (NotFoundException, LogicalException) as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)

        return send_file(
            BytesIO(file_dto.content),
            as_attachment=True,
            mimetype=file_dto.mimetype,
            attachment_filename=file_dto.name,
        )

    def delete(self, picture_name: str):
        try:
            self._storage_service.delete(picture_name)
        except (NotFoundException, LogicalException) as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)
        return jsonify_response({}, status_code=HTTPStatus.NO_CONTENT)
