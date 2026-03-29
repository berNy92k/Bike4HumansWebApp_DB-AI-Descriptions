import enum

from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    DELIVERY = "delivery"
    CANCELED = "canceled"
    FAILED = "failed"
    COMPLETED = "completed"


class Order(BaseModel):
    __tablename__ = "orders"

    order_id: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String, default="PLN", nullable=False)
    status: Mapped[str] = mapped_column(String, default=OrderStatus.PENDING.name, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), nullable=False)

    user = relationship("User")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="items")
    bike = relationship("Bike")
