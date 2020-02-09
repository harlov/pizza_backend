from typing import List
import abc

from pizza_app.core import models


class CurrencyRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def save(self, currency: models.Currency):
        ...

    @abc.abstractmethod
    def get(self, uid: str) -> models.Currency:
        ...

    @abc.abstractmethod
    def get_by_name(self, name: str) -> models.Currency:
        ...

    @abc.abstractmethod
    def get_list(self) -> List[models.Currency]:
        ...

    @abc.abstractmethod
    def save_rate(self, currency_rate: models.CurrencyRate):
        ...

    @abc.abstractmethod
    def get_rate(self, currency_1: models.Currency, currency_2: models.Currency) -> models.CurrencyRate:
        ...


class MenuItemRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def get(self, uid: str) -> models.MenuItem:
        ...

    @abc.abstractmethod
    def get_list(self) -> List[models.MenuItem]:
        ...

    @abc.abstractmethod
    def save(self, menu_item: models.MenuItem) -> models.MenuItem:
        ...


class CartRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def save(self, cart: models.Cart) -> models.Cart:
        ...

    @abc.abstractmethod
    def get(self, uid: str) -> models.Cart:
        ...


class ClientRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def save(self, client: models.Client) -> models.Client:
        ...

    @abc.abstractmethod
    def get_by_phone(self, phone: str) -> models.Client:
        ...


class OrderRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def save(self, order: models.Order) -> models.Order:
        ...

    @abc.abstractmethod
    def get(self, uid: str) -> models.Order:
        ...
