from sqlalchemy.orm import Session

from app.models.checkout import Checkout, CheckoutStatus


class CheckoutRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_checkout_by_id(self, checkout_id):
        return self.db.query(Checkout).where(Checkout.id == checkout_id).first()

    def get_cart_by_user_id_and_status(self, user_id: int, status: CheckoutStatus):
        return (self.db.query(Checkout)
                .where(Checkout.user_id == user_id)
                .where(Checkout.status == status.name)
                .first())

    def get_checkouts_paginated(self, page: int, size: int):
        query = self.db.query(Checkout).order_by(Checkout.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def create_or_update(self, checkout: Checkout):
        self.db.add(checkout)
        self.db.commit()
        self.db.refresh(checkout)

    def update_checkout(self, checkout):
        self.db.add(checkout)
        self.db.commit()

    def delete(self, checkout: Checkout):
        self.db.delete(checkout)
        self.db.commit()
