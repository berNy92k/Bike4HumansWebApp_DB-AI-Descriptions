from sqlalchemy.orm import Session

from app.models.user import Address


class AddressRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_address_by_id(self, address_id: int) -> Address | None:
        return self.db.query(Address).where(Address.id == address_id).first()

    def create_or_update(self, address: Address) -> None:
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
