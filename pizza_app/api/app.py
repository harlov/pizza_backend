from flask import Flask
from . import handlers
from . import error_handlers
from pizza_app.core.service import Service


def start(service: Service):
    app = Flask(__name__)

    handlers.bind_routes_to_app(app)
    handlers.service = service
    error_handlers.setup_handlers(app)

    app.run(debug=True)
