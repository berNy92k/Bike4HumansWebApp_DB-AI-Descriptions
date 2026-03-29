from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Role(BaseModel):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
