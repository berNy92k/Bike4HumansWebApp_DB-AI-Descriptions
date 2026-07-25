from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.models.order import Order, OrderItem, OrderStatus
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


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(Bike).delete()
    db_session.commit()

    yield

    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(Bike).delete()
    db_session.commit()


@pytest.fixture
def seeded_order(db_session, clean_tables):
    # Given
    bike = Bike(name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(bike)
    db_session.flush()

    order = Order(order_id="ORD00000001", user_id=1, currency="PLN", status=OrderStatus.PENDING.name,
                  total_price=100.0, payment_method_id=1)
    order.items.append(OrderItem(bike_id=bike.id, quantity=1))
    db_session.add(order)
    db_session.commit()

    return order


def test_delete_order_by_id_not_found(db_session):
    # Given
    service = AdminOrderService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.delete_order_by_id(999999)

    assert exc.value.status_code == 404


def test_generate_order_summary_caches_result(db_session, seeded_order):
    # Given
    mock_ai_summary_service = MagicMock()
    mock_ai_summary_service.generate_summary.return_value = "Podsumowanie zamówienia."
    service = AdminOrderService(db_session, ai_summary_service=mock_ai_summary_service)

    # When
    service.generate_order_summary(seeded_order.id)
    result = service.generate_order_summary(seeded_order.id)

    # Then
    assert result.summary == "Podsumowanie zamówienia."
    mock_ai_summary_service.generate_summary.assert_called_once()

    db_session.expire_all()
    cached_order = db_session.query(Order).filter(Order.id == seeded_order.id).first()
    assert cached_order.ai_summary == "Podsumowanie zamówienia."
    assert cached_order.ai_summary_generated_at is not None


def test_generate_order_summary_not_found(db_session):
    # Given
    service = AdminOrderService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.generate_order_summary(999999)

    assert exc.value.status_code == 404


def test_update_status_by_id_invalidates_cached_summary_on_status_change(db_session, seeded_order):
    # Given
    service = AdminOrderService(db_session)
    seeded_order.ai_summary = "Stare podsumowanie."
    db_session.commit()

    # When
    service.update_status_by_id(seeded_order.user_id, OrderStatus.DELIVERY.name, seeded_order.id)

    # Then
    db_session.expire_all()
    updated = db_session.query(Order).filter(Order.id == seeded_order.id).first()
    assert updated.ai_summary is None
    assert updated.ai_summary_generated_at is None


def test_update_status_by_id_keeps_cached_summary_when_status_unchanged(db_session, seeded_order):
    # Given
    service = AdminOrderService(db_session)
    seeded_order.ai_summary = "Stare podsumowanie."
    db_session.commit()

    # When
    service.update_status_by_id(seeded_order.user_id, OrderStatus.PENDING.name, seeded_order.id)

    # Then
    db_session.expire_all()
    updated = db_session.query(Order).filter(Order.id == seeded_order.id).first()
    assert updated.ai_summary == "Stare podsumowanie."
