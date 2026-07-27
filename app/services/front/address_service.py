from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import Address, AddressType
from app.repositories.address_repository import AddressRepository
from app.repositories.user_repository import UserRepository
from app.schemas.front.address.address_upsert_dto import AddressUpsertDto


class AddressService:

    def __init__(self, db: Session):
        self.address_repository = AddressRepository(db)
        self.user_repository = UserRepository(db)

    def get_my_address(self, user_id: int) -> Address:
        user = self.user_repository.get_user_by_id(user_id)
        if not user or not user.address_id:
            raise HTTPException(status_code=404, detail="Address not found")

        address = self.address_repository.get_address_by_id(user.address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        return address

    def save_my_address(self, user_id: int, address_upsert_dto: AddressUpsertDto) -> Address:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.address_id:
            address = self.address_repository.get_address_by_id(user.address_id)
            for field, value in address_upsert_dto.model_dump().items():
                setattr(address, field, value)
        else:
            address = Address(type=AddressType.SHIPPING.name, **address_upsert_dto.model_dump())

        self.address_repository.create_or_update(address)

        if not user.address_id:
            user.address_id = address.id
            self.user_repository.update_user(user)

        return address
