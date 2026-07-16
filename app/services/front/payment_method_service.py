from sqlalchemy.orm import Session

from app.models.payment_method import PaymentMethod
from app.repositories.payment_method_repository import PaymentMethodRepository


class PaymentMethodService:

    def __init__(self, db: Session):
        self.payment_method_repository = PaymentMethodRepository(db)

    def get_methods(self) -> list[PaymentMethod]:
        return self.payment_method_repository.get_methods()

    def get_method_by_id(self, payment_method_id: int) -> PaymentMethod:
        return self.payment_method_repository.get_method_by_id(payment_method_id)
