from typing import List
from typing import Optional
from uuid import UUID

from pizza_app.core import repositories, models
from sqlalchemy.orm import Session


class BaseAlchemyRepository:
    _session: Session

    def __init__(self, session: Session):
        self._session = session
        super().__init__()


class CurrencyRepository(repositories.CurrencyRepositoryABC, BaseAlchemyRepository):
    def get_by_name(self, name: str) -> models.Currency:
        return self._session.query(models.Currency).filter(
            models.Currency.name == name
        ).first()

    def get_list(self) -> List[models.Currency]:
        return list(self._session.query(models.Currency))

    def save(self, currency: models.Currency):
        self._session.add(currency)
        return currency

    def get(self, uid: str) -> models.Currency:
        return self._session.query(models.Currency).filter(models.Currency.uid == uid).first()

    def save_rate(self, currency_rate: models.CurrencyRate):
        self._session.add(currency_rate)

    def get_rate(self, currency_1: models.Currency, currency_2: models.Currency) -> models.CurrencyRate:
        return self._session.query(models.CurrencyRate).filter(
            models.CurrencyRate.first == currency_1,
            models.CurrencyRate.second == currency_2,
        ).first()


class CartRepository(repositories.CartRepositoryABC, BaseAlchemyRepository):
    def save(self, cart: models.Cart) -> models.Cart:
        self._session.add(cart)
        return cart

    def get(self, uid: UUID) -> models.Cart:
        return self._session.query(models.Cart).filter(models.Cart.uid == uid).first()


class MenuItemRepository(repositories.MenuItemRepositoryABC, BaseAlchemyRepository):
    def get(self, uid: str) -> models.MenuItem:
        return self._session.query(models.MenuItem).filter(models.MenuItem.uid == uid).first()

    def save(self, menu_item: models.MenuItem) -> models.MenuItem:
        self._session.add(menu_item)
        return menu_item

    def get_list(self) -> List[models.MenuItem]:
        return list(self._session.query(models.MenuItem).order_by(models.MenuItem.name))


class ClientRepository(repositories.ClientRepositoryABC, BaseAlchemyRepository):
    def save(self, client: models.Client) -> models.Client:
        self._session.add(client)
        return client

    def get_by_phone(self, phone: str) -> Optional[models.Client]:
        return self._session.query(models.Client).filter(models.Client.phone == phone).first()


class OrderRepository(repositories.OrderRepositoryABC, BaseAlchemyRepository):
    def get(self, uid: str) -> models.Order:
        return self._session.query(models.Order).filter(models.Order.uid == uid).first()

    def save(self, order: models.Order) -> models.Order:
        self._session.add(order)
        return order
