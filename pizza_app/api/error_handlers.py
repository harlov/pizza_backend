from flask import jsonify
from marshmallow.exceptions import ValidationError as SchemaValidationError
from pizza_app.core.exceptions import CoreException
from pizza_app.core.exceptions import EntityNotFound


def on_schema_errors(e):
    return jsonify(e.messages), 422


def on_entity_not_found(e):
    return jsonify({
        "error": "not found",
        "entity": e.entity,
        "uid": e.uid,
    }), 404


def on_core_errors(e):
    field = e.field if e.field is not None else "_schema"
    return jsonify({
        field: e.message
    })


def setup_handlers(app):
    app.register_error_handler(SchemaValidationError, on_schema_errors)
    app.register_error_handler(CoreException, on_core_errors)
    app.register_error_handler(EntityNotFound, on_entity_not_found)
