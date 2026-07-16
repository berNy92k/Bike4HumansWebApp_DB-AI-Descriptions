import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.models.checkout import Checkout, CheckoutItem, CheckoutStatus
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.order_repository import OrderRepository
from app.services.front.order_service import OrderService
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
    db_session.query(CheckoutItem).delete()
    db_session.query(Checkout).delete()
    db_session.query(Bike).delete()
    db_session.commit()

    yield

    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(CheckoutItem).delete()
    db_session.query(Checkout).delete()
    db_session.query(Bike).delete()
    db_session.commit()


@pytest.fixture
def seeded_pending_checkout(db_session, clean_tables):
    # Given
    bike = Bike(name="Trek Marlin 7", price=1000.0, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(bike)
    db_session.commit()

    checkout = Checkout(user_id=1, currency="PLN", status=CheckoutStatus.PENDING.name, total_price=2000.0,
                         payment_method_id=1)
    checkout.items.append(CheckoutItem(bike_id=bike.id, quantity=2))
    db_session.add(checkout)
    db_session.commit()

    return checkout


@pytest.fixture
def seeded_pending_order(db_session, clean_tables):
    # Given
    order = Order(order_id="ORD00000001", user_id=1, currency="PLN", status=OrderStatus.PENDING.name,
                  total_price=2000.0, payment_method_id=1)
    order.items.append(OrderItem(bike_id=1, quantity=2))
    db_session.add(order)
    db_session.commit()

    return order


def test_create_order(db_session, seeded_pending_checkout):
    # Given
    service = OrderService(db_session)
    order_repository = OrderRepository(db_session)

    # When
    service.create_order(user_id=1)

    # Then
    order = order_repository.get_order_by_user_id(1)
    assert order is not None
    assert order.total_price == 2000.0
    assert len(order.order_id) == 11
    assert len(order.items) == 1
    assert order.items[0].quantity == 2

    db_session.expire_all()
    checkout = db_session.get(Checkout, seeded_pending_checkout.id)
    assert checkout.status == CheckoutStatus.COMPLETED.name


def test_create_order_without_checkout(db_session, clean_tables):
    # Given
    service = OrderService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.create_order(user_id=99)

    assert exc.value.status_code == 404


def test_update_status(db_session, seeded_pending_order):
    # Given
    service = OrderService(db_session)

    # When
    result = service.update_status(user_id=1, status=OrderStatus.DELIVERY.name, previous_status=OrderStatus.PENDING.name)

    # Then
    assert result.status == OrderStatus.DELIVERY.name

    db_session.expire_all()
    updated = db_session.get(Order, seeded_pending_order.id)
    assert updated.status == OrderStatus.DELIVERY.name


def test_update_status_not_found(db_session, seeded_pending_order):
    # Given
    service = OrderService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.update_status(user_id=1, status=OrderStatus.DELIVERY.name, previous_status=OrderStatus.COMPLETED.name)

    assert exc.value.status_code == 404


def test_get_order_by_user_id_and_order_id(db_session, seeded_pending_order):
    # Given
    service = OrderService(db_session)

    # When
    result = service.get_order_by_user_id_and_order_id(1, "ORD00000001")

    # Then
    assert result.id == seeded_pending_order.id


def test_get_order_by_user_id_and_order_id_not_found(db_session, seeded_pending_order):
    # Given
    service = OrderService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_order_by_user_id_and_order_id(1, "UNKNOWN")

    assert exc.value.status_code == 404
