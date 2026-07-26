from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.front.payment_method.payment_method_read_dto import PaymentMethodReadDto
from app.services.front.payment_method_service import PaymentMethodService

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment methods"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PaymentMethodReadDto])
async def find_payment_methods(db: db_dependency):
    service = PaymentMethodService(db)
    return service.get_methods()


@router.get("/{payment_method_id}", status_code=status.HTTP_200_OK, response_model=PaymentMethodReadDto)
async def find_payment_method_by_id(payment_method_id: int, db: db_dependency):
    service = PaymentMethodService(db)
    method = service.get_method_by_id(payment_method_id)

    if not method:
        raise HTTPException(status_code=404, detail="Payment method not found")

    return method
