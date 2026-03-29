from sqlalchemy.orm import Session

from app.models.bike import Bike


class BikeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_bikes(self):
        return self.db.query(Bike).order_by(Bike.created_at.desc()).all()

    def get_last_x_bikes(self, size: int):
        return self.db.query(Bike).order_by(Bike.created_at.desc()).limit(size).all()

    def get_bikes_paginated(self, page: int, size: int):
        query = self.db.query(Bike).order_by(Bike.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def get_bike_by_id(self, bike_id):
        return self.db.query(Bike).where(Bike.id == bike_id).first()

    def create_bike(self, bike):
        self.db.add(bike)
        self.db.commit()

    def update_bike(self, bike):
        self.db.add(bike)
        self.db.commit()

    def delete(self, bike: Bike):
        self.db.delete(bike)
        self.db.commit()