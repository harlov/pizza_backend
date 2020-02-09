from __future__ import annotations

import abc

from pizza_app.core import repositories


class UnitOfWorkABC(abc.ABC):
    carts: repositories.CartRepositoryABC
    currencies: repositories.CurrencyRepositoryABC
    menu_items: repositories.MenuItemRepositoryABC
    clients: repositories.ClientRepositoryABC
    orders: repositories.OrderRepositoryABC

    def __init__(self,
                 carts: repositories.CartRepositoryABC,
                 currencies: repositories.CurrencyRepositoryABC,
                 menu_items: repositories.MenuItemRepositoryABC,
                 clients: repositories.ClientRepositoryABC,
                 orders: repositories.OrderRepositoryABC):
        self.carts = carts
        self.currencies = currencies
        self.menu_items = menu_items
        self.clients = clients
        self.orders = orders

    def __enter__(self) -> UnitOfWorkABC:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()

    @abc.abstractmethod
    def rollback(self):
        ...

    @abc.abstractmethod
    def commit(self):
        ...


class UnitOfWorkMangerABC(abc.ABC):
    def new(self) -> UnitOfWorkABC:
        return self._make_uow()

    @abc.abstractmethod
    def _make_uow(self):
        ...
