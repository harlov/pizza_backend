from pizza_app.core.service import Service
from pizza_app.infra import uow
from pizza_app import config

if __name__ == '__main__':

    service = Service(uow_manager=uow.UnitOfWorkManager(
        config.STORAGE_URI
    ))

    service.pre_fill_data()

    cart = service.create_cart()
    menu_items = service.get_menu_items()

    service.add_menu_item_to_cart(
        cart_uid=cart.uid,
        menu_item_uid=menu_items[0].uid
    )

    cart = service.get_cart(cart.uid)

    print(f'Cart {cart.uid}')
    print('--- items ---')
    for item in cart.items:
        print(f' {item.menu_item.name}: {item.quantity} pcs.')
