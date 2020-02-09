import pytest

from pizza_app.core import models
from pizza_app.core.service import Service
from pizza_app.infra.uow import UnitOfWorkManager


@pytest.fixture
def uow_manager(tmp_path):
    db_path = tmp_path / 'pizza.sqlite'
    return UnitOfWorkManager(
        uri=f'sqlite:///{db_path}'
    )


@pytest.fixture
def uow(uow_manager):
    with uow_manager.new() as uow:
        yield uow


@pytest.fixture
def service(uow_manager: uow):
    return Service(
        uow_manager=uow_manager
    )


@pytest.fixture
def pre_filled_data(service: Service):
    service.pre_fill_data()


@pytest.fixture
def cart(service):
    return service.create_cart()


@pytest.fixture
def eur_currency_uid():
    return models.make_uid()


@pytest.fixture
def eur_currency(uow_manager, eur_currency_uid):
    with uow_manager.new() as uow:
        obj = uow.currencies.save(models.Currency(
            uid=eur_currency_uid,
            name='EUR'
        ))
        uow.commit()
        return obj


@pytest.fixture
def menu_item(uow_manager, eur_currency_uid):
    with uow_manager.new() as uow:
        eur_currency = uow.currencies.get(eur_currency_uid)
        obj = uow.menu_items.save(models.MenuItem(
            uid=models.make_uid(),
            name='Test Item',
            price_value=10.0,
            price_currency=eur_currency,
        ))
        uow.commit()
        return obj


@pytest.fixture
def menu_item_2(uow_manager, eur_currency_uid):
    with uow_manager.new() as uow:
        eur_currency = uow.currencies.get(eur_currency_uid)
        obj = uow.menu_items.save(models.MenuItem(
            uid=models.make_uid(),
            name='Test Item 2',
            price_value=15.0,
            price_currency=eur_currency,
        ))
        uow.commit()
        return obj
