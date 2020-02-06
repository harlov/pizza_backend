from typing import List
from uuid import UUID

from pizza_app.core import repositories, models


class CartRepository(repositories.CartRepositoryABC):
    def create(self) -> models.Cart:
        pass

    def save(self, cart: models.Cart) -> None:
        pass

    def get(self, uid: UUID) -> models.Cart:
        pass


class MenuItemRepository(repositories.MenuItemRepositoryABC):
    def get_list(self) -> List[models.MenuItem]:
        pass

