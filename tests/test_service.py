import pytest

from pizza_app.core import models
from pizza_app.core import exceptions
from pizza_app.core.uow import UnitOfWorkABC
from pizza_app.core.service import Service


@pytest.mark.usefixtures('pre_filled_data')
def test_pre_filled_currencies(uow: UnitOfWorkABC):
    usd_currency = uow.currencies.get_by_name('USD')
    eur_currency = uow.currencies.get_by_name('EUR')

    assert usd_currency.name == 'USD'
    assert eur_currency.name == 'EUR'

    eur2usd_rate = uow.currencies.get_rate(eur_currency, usd_currency)

    assert eur2usd_rate.ratio == 1.09


@pytest.mark.usefixtures('pre_filled_data')
def test_pre_filled_menu_items(uow: UnitOfWorkABC):
    eur_currency = uow.currencies.get_by_name('EUR')
    menu_items = uow.menu_items.get_list()

    assert [(item.name, item.price_value, item.price_currency) for item in menu_items] == [
        ('Chili Salami', 3.75, eur_currency),
        ('French Fries', 2.5, eur_currency),
        ('Hawaii', 3.0, eur_currency),
        ('Kebab', 3.0, eur_currency),
        ('Margarita', 4.5, eur_currency),
        ('Meat', 3.95, eur_currency),
        ('Salami', 3.5, eur_currency),
        ('Seafood', 5.0, eur_currency),
        ('Tomato', 2.0, eur_currency),
        ('Vegan', 6.55, eur_currency),
    ]


def test_create_cart(service: Service):
    cart = service.create_cart()
    assert cart.status == models.CartStatus.STATUS_ACTIVE


def test_add_items_to_cart(service: Service, cart: models.Cart,
                           menu_item: models.MenuItem, menu_item_2: models.MenuItem):
    service.add_menu_item_to_cart(cart.uid, menu_item.uid, 1)
    cart_state = service.get_cart(cart.uid)

    assert len(cart_state.items) == 1
    assert cart_state.items[0].menu_item == menu_item
    assert cart_state.items[0].quantity == 1

    service.add_menu_item_to_cart(cart.uid, menu_item_2.uid, 2)
    cart_state = service.get_cart(cart.uid)

    assert len(cart_state.items) == 2
    assert cart_state.items[1].menu_item == menu_item_2
    assert cart_state.items[1].quantity == 2

    service.add_menu_item_to_cart(cart.uid, menu_item.uid, 2)
    cart_state = service.get_cart(cart.uid)

    assert len(cart_state.items) == 2
    assert cart_state.items[0].menu_item == menu_item
    assert cart_state.items[0].quantity == 3


def test_checkout(service: Service, cart: models.Cart, menu_item: models.MenuItem, menu_item_2: models.MenuItem, uow: UnitOfWorkABC) -> models.Order:
    fake_name = "Pikachu"
    fake_phone = "+7-900-800-8001"
    fake_address = "Moscow, Kremlin"

    service.add_menu_item_to_cart(cart.uid, menu_item.uid, 1)
    service.add_menu_item_to_cart(cart.uid, menu_item_2.uid, 2)
    order = service.checkout(cart.uid, fake_name, fake_phone, fake_address)
    order_state = uow.orders.get(order.uid)
    assert order_state is not None and order_state.uid == order.uid

    assert order_state.price_value == (
        menu_item.price_value +
        menu_item_2.price_value * 2 +
        3.0
    )
    assert order_state.client is not None

    client = uow.clients.get_by_phone("+7-900-800-8001")
    assert client == order_state.client
    assert order_state.address == fake_address == client.address
    assert order_state.phone == fake_phone == client.phone

    cart = uow.carts.get(cart.uid)
    assert cart.status == models.CartStatus.STATUS_PROCESSED

    with pytest.raises(exceptions.CoreException):  # second call checkout must fail
        service.checkout(cart.uid, fake_name, fake_phone, fake_address)
