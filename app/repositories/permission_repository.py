from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_codes(self, codes: list[str]) -> list[Permission]:
        return self.db.query(Permission).filter(Permission.code.in_(codes)).all()

    def get_all(self) -> list[Permission]:
        return self.db.query(Permission).all()
