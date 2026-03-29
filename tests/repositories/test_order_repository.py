import pytest

from app.models.order import Order, OrderStatus
from app.repositories.order_repository import OrderRepository
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
def clean_order_table(db_session):
    # Given
    db_session.query(Order).delete()
    db_session.commit()

    yield

    db_session.query(Order).delete()
    db_session.commit()


@pytest.fixture
def seeded_orders(db_session, clean_order_table):
    # Given
    orders = [
        Order(order_id="ORD00000001", user_id=1, currency="PLN", status=OrderStatus.PENDING.name, total_price=100.0, payment_method_id=1),
        Order(order_id="ORD00000002", user_id=2, currency="EUR", status=OrderStatus.COMPLETED.name, total_price=200.0, payment_method_id=2),
        Order(order_id="ORD00000003", user_id=3, currency="USD", status=OrderStatus.FAILED.name, total_price=300.0, payment_method_id=3),
    ]

    for order in orders:
        db_session.add(order)
    db_session.commit()

    return orders


def test_get_order_by_id(db_session, seeded_orders):
    # Given
    repo = OrderRepository(db_session)
    order_id = seeded_orders[0].id

    # When
    result = repo.get_order_by_id(order_id)

    # Then
    assert result is not None
    assert result.order_id == "ORD00000001"


def test_get_order_by_user_id(db_session, seeded_orders):
    # Given
    repo = OrderRepository(db_session)

    # When
    result = repo.get_order_by_user_id(2)

    # Then
    assert result is not None
    assert result.order_id == "ORD00000002"


def test_get_order_by_user_id_and_status(db_session, seeded_orders):
    # Given
    repo = OrderRepository(db_session)

    # When
    result = repo.get_order_by_user_id_and_status(1, OrderStatus.PENDING.name)

    # Then
    assert result is not None
    assert result.order_id == "ORD00000001"


def test_get_order_by_order_id_and_user_id(db_session, seeded_orders):
    # Given
    repo = OrderRepository(db_session)

    # When
    result = repo.get_order_by_order_id_and_user_id("ORD00000003", 3)

    # Then
    assert result is not None
    assert result.total_price == 300.0


def test_get_orders_paginated(db_session, seeded_orders):
    # Given
    repo = OrderRepository(db_session)

    # When
    items, total = repo.get_orders_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2


def test_create_update_delete_order(db_session, seeded_orders):
    # Given
    repo = OrderRepository(db_session)
    order = seeded_orders[0]

    # When
    repo.update_order(order)

    # Then
    assert repo.get_order_by_id(order.id) is not None

    # When
    repo.delete(order)

    # Then
    assert repo.get_order_by_id(order.id) is None
