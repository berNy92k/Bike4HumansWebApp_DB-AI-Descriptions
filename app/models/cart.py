import enum

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class CartStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String, default="PLN", nullable=False)
    status: Mapped[str] = mapped_column(String, default=CartStatus.PENDING.name, nullable=False)

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False, index=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    bike = relationship("Bike")
