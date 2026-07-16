import pytest
from fastapi import HTTPException

from app.services.admin.admin_order_service import AdminOrderService
from tests.database.database import override_get_db


@pytest.fixture
def db_session():
    db_gen = override_get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        db.close()


def test_delete_order_by_id_not_found(db_session):
    # Given
    service = AdminOrderService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.delete_order_by_id(999999)

    assert exc.value.status_code == 404
