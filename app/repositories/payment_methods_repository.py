from sqlalchemy.orm import Session

from app.models import PaymentMethod


class PaymentMethodRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_methods(self):
        return self.db.query(PaymentMethod).all()

    def get_method_by_id(self, payment_method_id: int):
        return self.db.query(PaymentMethod).where(PaymentMethod.id == payment_method_id).first()
