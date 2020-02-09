from flask import Flask
from flask_cors import CORS

from . import handlers
from . import error_handlers
from pizza_app.core.service import Service


def start(service: Service):
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'

    CORS(app)

    handlers.bind_routes_to_app(app)
    handlers.service = service
    error_handlers.setup_handlers(app)

    app.run(debug=True)
