import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.checkout import Checkout, CheckoutItem, CheckoutStatus
from app.models.order import Order, OrderItem, OrderStatus
from app.services.auth.auth_service import get_current_user
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
def client():
    # Given
    app.dependency_overrides[get_current_user] = lambda: {"user_id": 1, "role_id": 4}
    client = TestClient(app)

    yield client

    app.dependency_overrides.pop(get_current_user, None)


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

    checkout = Checkout(user_id=1, currency="PLN", status=CheckoutStatus.PENDING.name, total_price=1000.0,
                         payment_method_id=1)
    checkout.items.append(CheckoutItem(bike_id=bike.id, quantity=1))
    db_session.add(checkout)
    db_session.commit()

    return checkout


@pytest.fixture
def seeded_pending_order(db_session, clean_tables):
    # Given
    order = Order(order_id="ORD00000001", user_id=1, currency="PLN", status=OrderStatus.PENDING.name,
                  total_price=1000.0, payment_method_id=1)
    order.items.append(OrderItem(bike_id=1, quantity=1))
    db_session.add(order)
    db_session.commit()

    return order


def test_create_order(client, seeded_pending_checkout, db_session):
    # Given

    # When
    response = client.post("/order/")

    # Then
    assert response.status_code == 201
    order = db_session.query(Order).filter(Order.user_id == 1).first()
    assert order is not None
    assert order.total_price == 1000.0


def test_create_order_without_checkout(client, clean_tables):
    # Given

    # When
    response = client.post("/order/")

    # Then
    assert response.status_code == 404


def test_update_order_status(client, seeded_pending_order, db_session):
    # Given

    # When
    response = client.put("/order/", params={"status": "delivery", "previous_status": "pending"})

    # Then
    assert response.status_code == 201
    assert response.json()["order_id"] == "ORD00000001"
    db_session.expire_all()
    updated = db_session.query(Order).filter(Order.id == seeded_pending_order.id).first()
    assert updated.status == OrderStatus.DELIVERY.name


def test_update_order_status_not_found(client, seeded_pending_order):
    # Given

    # When
    response = client.put("/order/", params={"status": "delivery", "previous_status": "completed"})

    # Then
    assert response.status_code == 404
