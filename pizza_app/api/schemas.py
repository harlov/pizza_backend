from marshmallow import Schema, fields, pprint, validate


class CartItemSchema(Schema):
    uid = fields.Str(dump_only=True)
    menu_item_uid = fields.Str(required=True)
    quantity = fields.Integer(required=True)


class CartSchema(Schema):
    uid = fields.Str(dump_only=True)
    status = fields.Integer(dump_only=True)
    items = fields.Nested(nested=CartItemSchema, many=True, dump_only=True)


cart_item_schema = CartItemSchema()
cart_schema = CartSchema()
