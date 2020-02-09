from __future__ import annotations

import enum
from uuid import uuid4
from typing import List
from dataclasses import dataclass

from pizza_app.core import exceptions


def make_uid() -> str:
    return str(uuid4())


@dataclass
class Currency:
    uid: str
    name: str


@dataclass
class CurrencyRate:
    """
    To convert 'first' to 'second' we need to multiple 'first' currency amount on ratio.
    And otherwise: to convert 'second' to 'first' we need to divide 'second' amount on ratio
    """
    uid: str
    first: Currency
    second: Currency
    ratio: float

    def convert_first_to_second(self, amount: float):
        return amount * self.ratio

    def convert_second_to_first(self, amount: float):
        return amount / self.ratio


@dataclass
class MenuItem:
    uid: str
    name: str
    price_value: float
    price_currency: Currency

    def __eq__(self, other):
        return self.uid == other.uid


@dataclass
class Client:
    uid: str
    name: str
    address: str
    phone: str


class CartStatus(enum.IntEnum):
    STATUS_ACTIVE = 1
    STATUS_PROCESSED = 2


@dataclass
class CartItem:
    uid: str
    cart: Cart
    menu_item: MenuItem
    quantity: int


@dataclass
class Cart:
    uid: str
    status: CartStatus
    items: List[CartItem]

    def __post_init__(self):
        self.items = []

    def add_item(self, menu_item: MenuItem, quantity: int):
        if quantity <= 0:
            raise exceptions.CoreException(exceptions.QUANTITY_MUST_BE_POSITIVE, field="quantity")

        for item in self.items:
            if item.menu_item != menu_item:
                continue

            item.quantity += quantity
            return

        self.items.append(CartItem(
            uid=make_uid(),
            cart=self,
            menu_item=menu_item,
            quantity=quantity,
        ))

    def delete_item(self, menu_item: MenuItem, quantity: int):
        if quantity <= 0:
            raise exceptions.CoreException(exceptions.QUANTITY_MUST_BE_POSITIVE, field="quantity")

        for item in self.items:
            if item.menu_item != menu_item:
                continue

            item.quantity -= quantity
            if item.quantity <= 0:
                self.items.remove(item)


@dataclass
class Order:
    client: Client
    cart: Cart
    price_value: float
    price_currency: Currency

