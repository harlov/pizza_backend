from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, ForeignKey, Float,
    event,
)
from sqlalchemy.orm import mapper, relationship

from pizza_app.core import models

metadata = MetaData()


def _get_pk_column():
    return Column('uid', String, primary_key=True)


currencies = Table(
    'currencies', metadata,
    _get_pk_column(),
    Column('name', String)
)

currencies_rates = Table(
    'currencies_rates', metadata,
    _get_pk_column(),
    Column('first_uid', ForeignKey('currencies.uid')),
    Column('second_uid', ForeignKey('currencies.uid')),
    Column('ratio', Float)
)


menu_items = Table(
    'menu_items', metadata,
    _get_pk_column(),
    Column('name', String),
    Column('price_value', Float),
    Column('price_currency_uid', ForeignKey('currencies.uid')),
)


carts = Table(
    'carts', metadata,
    _get_pk_column(),
    Column('status', Integer),
)

cart_items = Table(
    'cart_items', metadata,
    _get_pk_column(),
    Column('cart_uid', ForeignKey('carts.uid')),
    Column('menu_item_uid', ForeignKey('menu_items.uid')),
    Column('quantity', Integer),
)


clients = Table(
    'clients', metadata,
    _get_pk_column(),
    Column('name',  String),
    Column('phone', String),
    Column('address', String),
)

orders = Table(
    'orders', metadata,
    _get_pk_column(),
    Column('client_uid', ForeignKey('clients.uid')),
    Column('cart_uid', ForeignKey('carts.uid')),
    Column('phone', String),
    Column('address', String),
    Column('price_value', Float),
    Column('price_currency_uid', ForeignKey('currencies.uid'))
)

_mappers_was_bind = False


def bind_mappers():
    global _mappers_was_bind
    if _mappers_was_bind:
        return

    carts_mapper = mapper(models.Cart, carts)
    currencies_mapper = mapper(models.Currency, currencies)
    currencies_rates_mapper = mapper(models.CurrencyRate, currencies_rates, properties={
        'first': relationship(currencies_mapper, foreign_keys=(currencies_rates.c.first_uid,)),
        'second': relationship(currencies_mapper, foreign_keys=(currencies_rates.c.second_uid,)),
    })
    menu_items_mapper = mapper(models.MenuItem, menu_items, properties={
        'price_currency': relationship(currencies_mapper, foreign_keys=(menu_items.c.price_currency_uid,))
    })

    cart_items_mapper = mapper(models.CartItem, cart_items, properties={
        'cart': relationship(
            carts_mapper,
            foreign_keys=(cart_items.c.cart_uid,),
            backref='items',
            lazy='joined'
        ),
        'menu_item': relationship(
            menu_items_mapper,
            foreign_keys=(cart_items.c.menu_item_uid,)
        )
    })

    clients_mapper = mapper(models.Client, clients)
    orders_mapper = mapper(models.Order, orders, properties={
        'client': relationship(
            clients_mapper,
            foreign_keys=(orders.c.client_uid,)
        ),
        'cart': relationship(
            carts_mapper,
            foreign_keys=(orders.c.cart_uid,)
        )
    })

    _mappers_was_bind = True


def create_tables(engine):
    metadata.create_all(bind=engine)
