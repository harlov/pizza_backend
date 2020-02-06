from typing import List
from uuid import UUID
import abc

from pizza_app.core import models


class MenuItemRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def get_list(self) -> List[models.MenuItem]:
        ...


class CartRepositoryABC(abc.ABC):
    @abc.abstractmethod
    def create(self) -> models.Cart:
        ...

    @abc.abstractmethod
    def save(self, cart: models.Cart) -> None:
        ...

    @abc.abstractmethod
    def get(self, uid: UUID) -> models.Cart:
        ...
