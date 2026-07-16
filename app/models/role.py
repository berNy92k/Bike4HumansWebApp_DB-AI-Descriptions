from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel
from app.models.permission import Permission, role_permission


class Role(BaseModel):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    permissions: Mapped[list[Permission]] = relationship("Permission", secondary=role_permission, back_populates="roles")

    def has_permission(self, code: str) -> bool:
        return any(p.code == code for p in self.permissions)
