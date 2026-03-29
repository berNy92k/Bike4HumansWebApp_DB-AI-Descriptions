import enum

from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class CheckoutStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Checkout(BaseModel):
    __tablename__ = "checkouts"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True, unique=True)
    currency: Mapped[str] = mapped_column(String, default="PLN", nullable=False)
    status: Mapped[str] = mapped_column(String, default="PENDING", nullable=False)
    total_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), nullable=False)

    user = relationship("User")
    items = relationship("CheckoutItem", back_populates="checkout", cascade="all, delete-orphan")


class CheckoutItem(BaseModel):
    __tablename__ = "checkout_items"

    checkout_id: Mapped[int] = mapped_column(ForeignKey("checkouts.id"), nullable=False, index=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    checkout = relationship("Checkout", back_populates="items")
    bike = relationship("Bike")
