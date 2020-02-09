from flask import Flask, jsonify, request
from pizza_app.core.service import Service
from . import schemas

_routes_to_bind = []

service: Service = None

empty_response = "{}"


def route(rule, **options):
    def decorator(f):
        endpoint = options.pop("endpoint", None)
        _routes_to_bind.append((rule, endpoint, f, options))
        return f

    return decorator


def bind_routes_to_app(app: Flask):
    for rule, endpoint, f, options in _routes_to_bind:
        app.add_url_rule(rule, endpoint, f, **options)


@route('/api/v1/menu/', methods=['GET'])
def list_menu():
    return jsonify(service.get_menu_items())


@route('/api/v1/cart/<uid>', methods=['GET'])
def get_cart(uid):
    return jsonify(
        schemas.cart_schema.dump(service.get_cart(uid))
    )


@route('/api/v1/cart', methods=['PUT'])
def create_cart():
    return jsonify(service.create_cart())


@route('/api/v1/cart/<uid>/items', methods=['PUT'])
def add_item_to_cart(uid):
    data = schemas.cart_item_schema.load(
        request.get_json()
    )
    service.add_menu_item_to_cart(uid, data['menu_item_uid'], data['quantity'])
    return empty_response


@route('/api/v1/cart/<uid>/items', methods=['DELETE'])
def delete_item_from_cart(uid):
    data = schemas.cart_item_schema.load(
        request.get_json()
    )
    service.delete_menu_item_from_cart(uid, data['menu_item_uid'], data['quantity'])
    return empty_response
