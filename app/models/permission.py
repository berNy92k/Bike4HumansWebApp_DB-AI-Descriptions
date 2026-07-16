from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.base_model import BaseModel

role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)


class PermissionCode:
    ADMIN_PANEL_ACCESS = "ADMIN_PANEL_ACCESS"
    SUPER_ADMIN = "SUPER_ADMIN"


class Permission(BaseModel):
    __tablename__ = "permission"

    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    roles: Mapped[list["Role"]] = relationship("Role", secondary=role_permission, back_populates="permissions")
