from dataclasses import asdict
from http import HTTPStatus
from json import JSONDecodeError

from flask import current_app, request
from flask.views import MethodView
from pydantic import ValidationError, parse_raw_as
from werkzeug.exceptions import BadRequest

from api import logger
from api.dtos import PictureDTO
from api.exceptions import AlreadyExistException
from api.views.serializers.picture import GetPictureSerializer, PictureSerializer
from api.views.utils import json_response, jsonify_response, prepare_data


class PictureListView(MethodView):

    def __init__(self):
        self._storage_service = current_app.domain_services.storage_service()
        self._subscription_service = current_app.domain_services.subscription_service()

    def post(self):
        image = request.files["file"]
        try:
            data = prepare_data(request.form, image)
            serialized = parse_raw_as(PictureSerializer, data)
        except JSONDecodeError as exception:
            raise BadRequest(exception.msg)
        except ValidationError as exception:
            return json_response(exception.json(), status_code=HTTPStatus.BAD_REQUEST)

        picture_dto = PictureDTO(**serialized.dict())
        picture_dto.content = image.read()

        try:
            picture_entity = self._storage_service.upload(picture_dto)
        except AlreadyExistException as exception:
            return jsonify_response(exception.msg, status_code=HTTPStatus.BAD_REQUEST)

        logger.debug(f"File {picture_dto.name} has been uploaded.")

        self._subscription_service.message_to_queue(picture_dto)

        serialized = GetPictureSerializer(**asdict(picture_entity))
        return json_response(serialized.json(), status_code=HTTPStatus.CREATED)
