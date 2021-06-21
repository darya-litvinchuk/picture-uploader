from http import HTTPStatus

import psycopg2
from flask.views import MethodView

from api import get_settings
from api.views.utils import jsonify_response


class HealthCheckView(MethodView):
    @staticmethod
    def get(settings=get_settings()):
        """ Check connection to postgres database. """
        db_settings = settings.database
        try:
            psycopg2.connect(
                host=db_settings.host,
                port=db_settings.port,
                dbname=db_settings.work_db,
                user=db_settings.work_user,
                password=db_settings.work_user_password,
            )
        except Exception as exception:
            return jsonify_response(
                {"detail": f"Can't connect to database: {exception}"},
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            )
        return jsonify_response({})
