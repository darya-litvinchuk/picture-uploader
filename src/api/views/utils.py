import json
from typing import Dict, List, Union

from flask import Response, jsonify
from werkzeug.datastructures import FileStorage

JSON = "application/json"


def prepare_data(raw_data: str, image: FileStorage) -> str:
    data = dict(raw_data)
    data["mimetype"] = image.content_type
    return json.dumps(data)


def jsonify_response(data: Union[List, Dict], status_code: int = 200) -> Response:
    res = jsonify(data)
    res.status_code = status_code

    return res


def json_response(data: str, status_code: int = 200, mimetype: str = JSON) -> Response:
    return Response(data, mimetype=mimetype, status=status_code)
