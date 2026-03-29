from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_roles(self):
        return self.db.query(Role).order_by(Role.id.desc()).all()

    def get_roles_paginated(self, page: int, size: int):
        query = self.db.query(Role).order_by(Role.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def get_role_by_id(self, role_id) -> Role | None:
        return self.db.query(Role).where(Role.id == role_id).first()

    def create_role(self, role: Role):
        self.db.add(role)
        self.db.commit()

    def update_role(self, role):
        self.db.add(role)
        self.db.commit()

    def delete_role(self, role):
        self.db.delete(role)
        self.db.commit()
