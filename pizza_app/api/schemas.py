from marshmallow import Schema, fields, pprint, validate


class CurrencySchema(Schema):
    uid = fields.Str()
    name = fields.Str()


class MenuItemSchema(Schema):
    uid = fields.Str(dump_only=True)
    name = fields.String()
    price_value = fields.Float()
    price_currency = fields.Nested(nested=CurrencySchema)


class CartItemSchema(Schema):
    uid = fields.Str(dump_only=True)
    menu_item = fields.Nested(nested=MenuItemSchema)
    menu_item_uid = fields.Str(required=True, load_only=True)
    quantity = fields.Integer(required=True)


class CartSchema(Schema):
    uid = fields.Str(dump_only=True)
    status = fields.Integer(dump_only=True)
    items = fields.Nested(nested=CartItemSchema, many=True, dump_only=True)
    total_sum = fields.Float(dump_only=True)
    delivery_cost = fields.Float(dump_only=True)


class CheckoutSchema(Schema):
    client_name = fields.Str()
    client_phone = fields.Str()
    client_address = fields.Str()


menu_item_schema = MenuItemSchema()
cart_item_schema = CartItemSchema()
cart_schema = CartSchema()
checkout_schema = CheckoutSchema()
