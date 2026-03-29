from sqlalchemy.orm import Session

from app.models.manufacturer import Manufacturer


class ManufacturerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_manufacturers(self):
        return self.db.query(Manufacturer).all()

    def get_manufacturers_paginated(self, page: int, size: int):
        query = self.db.query(Manufacturer).order_by(Manufacturer.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def get_manufacturer_by_id(self, manufacturer_id):
        return self.db.query(Manufacturer).where(Manufacturer.id == manufacturer_id).first()

    def create_manufacturer(self, manufacturer):
        self.db.add(manufacturer)
        self.db.commit()

    def update_manufacturer(self, manufacturer):
        self.db.add(manufacturer)
        self.db.commit()

    def delete(self, manufacturer: Manufacturer):
        self.db.delete(manufacturer)
        self.db.commit()
