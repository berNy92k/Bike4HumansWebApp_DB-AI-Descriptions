import secrets
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.checkout import Checkout, CheckoutStatus
from app.models.order import OrderItem, Order, OrderStatus
from app.repositories.bike_repository import BikeRepository
from app.repositories.checkout_repository import CheckoutRepository
from app.repositories.order_repository import OrderRepository


class OrderService:

    def __init__(self, db: Session):
        self.bike_repository = BikeRepository(db)
        self.order_repository = OrderRepository(db)
        self.checkout_repository = CheckoutRepository(db)

    def _generate_order_id(self, length: int = 11) -> str:
        alphabet = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def create_order(self, user_id: int):
        checkout: Checkout = self.checkout_repository.get_cart_by_user_id_and_status(user_id, CheckoutStatus.PENDING)
        if not checkout or not checkout.items or len(checkout.items) == 0:
            raise HTTPException(status_code=404, detail="Checkout not found or empty")

        order_items: list[OrderItem] = []
        for item in checkout.items:
            order_items.append(OrderItem(
                bike_id=item.bike_id,
                quantity=item.quantity
            ))

        order = Order(
            order_id=self._generate_order_id(11),
            user_id=checkout.user_id,
            currency=checkout.currency,
            payment_method_id=1,
            total_price=checkout.total_price,
        )
        order.items = order_items

        self.order_repository.create_or_update(order)

        checkout.status = CheckoutStatus.COMPLETED.name
        self.checkout_repository.create_or_update(checkout)

    def update_status(self, user_id: int, status: OrderStatus, statusPrevious: OrderStatus):
        order: Order = self.order_repository.get_order_by_user_id_and_status(user_id, statusPrevious)
        if not order or not order.items or len(order.items) == 0:
            raise HTTPException(status_code=404, detail="Order not found or empty")

        order.status = status
        self.order_repository.create_or_update(order)
        return order

    def get_order_by_user_id_and_order_id(self, user_id: int, orderId: str):
        order: Order = self.order_repository.get_order_by_order_id_and_user_id(orderId, user_id)

        if not order:
            raise HTTPException(status_code=404, detail="Checkout not found")

        return order
