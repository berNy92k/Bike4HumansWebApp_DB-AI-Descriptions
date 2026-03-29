from sqlalchemy.orm import Session

from app.models.cart import Cart, CartStatus


class CartRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_id(self, cart_id):
        return self.db.query(Cart).where(Cart.id == cart_id).first()

    def get_cart_by_user_id(self, user_id: int):
        return self.db.query(Cart).where(Cart.user_id == user_id).first()

    def get_cart_by_user_id_and_status(self, user_id: int, status: CartStatus):
        return (self.db.query(Cart)
                .where(Cart.user_id == user_id)
                .where(Cart.status == status.name)
                .first())

    def get_carts_paginated(self, page: int, size: int):
        query = self.db.query(Cart).order_by(Cart.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def create_or_update(self, cart: Cart):
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)

    def update_cart(self, cart):
        self.db.add(cart)
        self.db.commit()

    def delete(self, cart: Cart):
        self.db.delete(cart)
        self.db.commit()
