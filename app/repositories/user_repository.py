from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).order_by(User.created_at.desc()).all()

    def get_users_paginated(self, page: int, size: int):
        query = self.db.query(User).order_by(User.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def get_user_by_id(self, user_id):
        return self.db.query(User).where(User.id == user_id).first()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()

    def update_user(self, user: User):
        self.db.add(user)
        self.db.commit()

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()

    def find_user_by_username(self, username):
        return self.db.query(User).where(User.username == username).first()
