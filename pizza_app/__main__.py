from pizza_app.core.service import Service
from pizza_app.infra import repositories


if __name__ == '__main__':
    cart_repository = repositories.CartRepository()
    menu_item_repository = repositories.MenuItemRepository()

    service = Service(
        cart_repo=cart_repository,
        menu_item_repo=menu_item_repository,
    )

    cart = service.create_cart()

    print(cart)
