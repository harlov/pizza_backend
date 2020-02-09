from typing import List

from pizza_app.core import models
from pizza_app.core.uow import UnitOfWorkMangerABC, UnitOfWorkABC


class Service:
    uow_manager: UnitOfWorkMangerABC

    def __init__(self, uow_manager: UnitOfWorkMangerABC):
        self.uow_manager = uow_manager

    def get_menu_items(self) -> List[models.MenuItem]:
        with self.uow_manager.new() as uow:
            return uow.menu_items.get_list()

    def create_cart(self) -> models.Cart:
        with self.uow_manager.new() as uow:
            cart = models.Cart(
                uid=models.make_uid(),
                items=[],
                status=models.CartStatus.STATUS_ACTIVE,
            )
            cart = uow.carts.save(cart)
            uow.commit()
            return cart

    def get_cart(self, uid: str) -> models.Cart:
        with self.uow_manager.new() as uow:
            return uow.carts.get(uid)

    def add_menu_item_to_cart(self, cart_uid: str, menu_item_uid: str, quantity: int = 1):
        with self.uow_manager.new() as uow:
            cart = uow.carts.get(cart_uid)
            menu_item = uow.menu_items.get(menu_item_uid)
            cart.add_item(
                menu_item=menu_item,
                quantity=quantity,
            )
            uow.commit()

    def pre_fill_data(self):
        with self.uow_manager.new() as uow:
            self._pre_fill_currencies(uow)
            self._pre_fill_menu(uow)
            uow.commit()

    def _pre_fill_currencies(self, uow: UnitOfWorkABC):
        if uow.currencies.get_list():
            return

        eur_curr = uow.currencies.save(
            models.Currency(uid=models.make_uid(), name='EUR')
        )
        usd_curr = uow.currencies.save(
            models.Currency(uid=models.make_uid(), name='USD')
        )

        uow.currencies.save_rate(
            models.CurrencyRate(
                uid=models.make_uid(),
                first=eur_curr,
                second=usd_curr,
                ratio=1.09
            )
        )

    def _pre_fill_menu(self, uow: UnitOfWorkABC):
        if uow.menu_items.get_list():
            return

        eur_currency = uow.currencies.get_by_name('EUR')

        for data in [
            ('Salami', 3.5),
            ('Chili Salami', 3.75),
            ('Hawaii', 3.0),
            ('Meat', 3.95),
            ('Tomato', 2.0),
            ('Vegan', 6.55),
            ('Seafood', 5.0),
            ('Margarita', 4.5),
            ('Kebab', 3.0),
            ('French Fries', 2.5)
        ]:
            uow.menu_items.save(models.MenuItem(
                uid=models.make_uid(),
                name=data[0],
                price_value=data[1],
                price_currency=eur_currency
            ))
