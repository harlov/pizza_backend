from typing import List
from uuid import UUID

from pizza_app.core import models
from pizza_app.core import repositories


class Service:
    menu_item_repo: repositories.MenuItemRepositoryABC
    cart_repo: repositories.CartRepositoryABC

    def __init__(self, menu_item_repo: repositories.MenuItemRepositoryABC, cart_repo: repositories.CartRepositoryABC):
        self.menu_item_repo = menu_item_repo
        self.cart_repo = cart_repo

    def get_menu_items(self) -> List[models.MenuItem]:
        return self.menu_item_repo.get_list()

    def create_cart(self) -> models.Cart:
        return self.cart_repo.create()

    def get_cart(self, uid: UUID) -> models.Cart:
        return self.cart_repo.get(uid)

    def add_menu_item_to_cart(self):
        pass