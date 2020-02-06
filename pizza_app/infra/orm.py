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
    Column('first', ForeignKey('currencies.uid')),
    Column('second', ForeignKey('currencies.uid')),
    Column('ratio', Float)
)


menu_items = Table(
    'menu_items', metadata,
    _get_pk_column(),
    Column('price_value', Float),
    Column('price_currency', ForeignKey('currencies.uid')),
)


carts = Table(
    'carts', metadata,
    _get_pk_column(),
    Column('status', Integer),
)


def bind_mappers():
    carts_mapper = mapper(models.Cart, carts)
    menu_items_mapper = mapper(models.MenuItem, menu_items)
