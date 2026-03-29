from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import CartItem
from app.models.cart import Cart, CartStatus
from app.repositories.bike_repository import BikeRepository
from app.repositories.cart_repository import CartRepository


class CartService:

    def __init__(self, db: Session):
        self.cart_repository = CartRepository(db)
        self.bike_repository = BikeRepository(db)

    def add_item_to_cart(self, user_id: int, bike_id: int):
        bike = self.bike_repository.get_bike_by_id(bike_id)
        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        cart = self.cart_repository.get_cart_by_user_id_and_status(user_id, CartStatus.PENDING)
        if not cart:
            cart = Cart(
                user_id=user_id,
                currency="PLN",
                status="PENDING"
            )
            cart.items.append(CartItem(bike_id=bike_id, quantity=1))
        else:
            item_updated: bool = False
            for item in cart.items:
                if item.bike_id == bike_id:
                    item.quantity += 1
                    item_updated = True

            if not item_updated:
                cart.items.append(CartItem(bike_id=bike_id, quantity=1))

        self.cart_repository.create_or_update(cart)

    def get_cart_by_user_id_and_pending_status(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user_id_and_status(user_id, CartStatus.PENDING)

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        return cart
