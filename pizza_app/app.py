from pizza_app.core.service import Service
from pizza_app.infra import uow
from pizza_app import config
from pizza_app.api import app as rest_app


def start():
    service = Service(uow_manager=uow.UnitOfWorkManager(
        config.STORAGE_URI
    ))
    service.pre_fill_data()
    rest_app.start(service)

