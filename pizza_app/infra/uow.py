from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


from pizza_app.core.uow import UnitOfWorkMangerABC
from pizza_app.core.uow import UnitOfWorkABC
from pizza_app.infra import repositories
from pizza_app.infra import orm


SessionMakerType = Callable[[], Session]


class UnitOfWork(UnitOfWorkABC):
    _session: Session

    def __init__(self, session: Session):
        self._session = session
        super().__init__(
            carts=repositories.CartRepository(session),
            currencies=repositories.CurrencyRepository(session),
            menu_items=repositories.MenuItemRepository(session),
            clients=repositories.ClientRepository(session),
            orders=repositories.OrderRepository(session),
        )

    def rollback(self):
        self._session.rollback()

    def commit(self):
        self._session.commit()


class UnitOfWorkManager(UnitOfWorkMangerABC):
    _engine: engine.Engine
    _session_maker: SessionMakerType

    def __init__(self, uri: str):
        self._engine = create_engine(uri)
        self._session_maker = sessionmaker(bind=self._engine, expire_on_commit=False)
        orm.bind_mappers()
        orm.create_tables(self._engine)

    def _make_uow(self) -> UnitOfWork:
        return UnitOfWork(session=self._session_maker())
