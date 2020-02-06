import enum
from uuid import UUID
from typing import List
from dataclasses import dataclass


@dataclass
class Currency:
    uid: UUID
    name: str


@dataclass
class CurrencyRate:
    uid: UUID
    first: Currency
    second: Currency
    ratio: float


@dataclass
class MenuItem:
    uid: UUID
    name: str
    price_value: float
    price_currency: Currency


@dataclass
class Client:
    uid: UUID
    name: str
    address: str
    phone: str


class CartStatus(enum.IntEnum):
    STATUS_ACTIVE = 1
    STATUS_PROCESSED = 2


@dataclass
class CartItem:
    menu_item: MenuItem
    quantity: int


@dataclass
class Cart:
    status: CartStatus
    items: List[CartItem]


@dataclass
class Order:
    client: Client
    cart: Cart
    price_value: float
    price_currency: Currency

