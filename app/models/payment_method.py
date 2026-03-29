from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class PaymentMethod(BaseModel):
    __tablename__ = "payment_methods"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
