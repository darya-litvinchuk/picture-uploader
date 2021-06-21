from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions

from api.config import get_settings, APP_URL_PREFIX
from api.containers import DomainServices, Core
from api.views.urls import bp as rules_bp


def configure_settings(app):
    settings = get_settings()

    Core.config.from_dict(settings.dict())

    app.config.from_object(settings)


def _json_error_handler(error):
    error_json = jsonify(message=error.description)
    error_json.status_code = error.code
    return error_json


def register_error_handlers(app):
    """ Default error handler. """
    errors = default_exceptions.values()
    for error in errors:
        app.register_error_handler(error, _json_error_handler)


def register_extensions(app):
    app.domain_services = DomainServices
    app.settings = Core


def register_blueprints(app):
    app.register_blueprint(rules_bp, url_prefix=APP_URL_PREFIX)


def register_schedulers(app):
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler(daemon=True)

    _subscription_service = app.domain_services.subscription_service()
    scheduler.add_job(_subscription_service.message_to_topic, "interval", minutes=1)
    scheduler.start()


def create_app():
    """ Construct the core application. """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    configure_settings(app)

    with app.app_context():
        register_error_handlers(app)
        register_extensions(app)
        register_blueprints(app)

    register_schedulers(app)

    return app
