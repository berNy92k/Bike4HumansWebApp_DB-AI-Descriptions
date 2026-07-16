import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.cart import Cart, CartItem, CartStatus
from app.models.checkout import Checkout, CheckoutItem
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
    db_session.query(CheckoutItem).delete()
    db_session.query(Checkout).delete()
    db_session.query(CartItem).delete()
    db_session.query(Cart).delete()
    db_session.query(Bike).delete()
    db_session.commit()

    yield

    db_session.query(CheckoutItem).delete()
    db_session.query(Checkout).delete()
    db_session.query(CartItem).delete()
    db_session.query(Cart).delete()
    db_session.query(Bike).delete()
    db_session.commit()


@pytest.fixture
def seeded_pending_cart(db_session, clean_tables):
    # Given
    bike = Bike(name="Trek Marlin 7", price=1000.0, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(bike)
    db_session.commit()

    cart = Cart(user_id=1, currency="PLN", status=CartStatus.PENDING.name)
    cart.items.append(CartItem(bike_id=bike.id, quantity=1))
    db_session.add(cart)
    db_session.commit()

    return cart


def test_create_checkout(client, seeded_pending_cart, db_session):
    # Given

    # When
    response = client.post("/checkout/")

    # Then
    assert response.status_code == 201
    checkout = db_session.query(Checkout).filter(Checkout.user_id == 1).first()
    assert checkout is not None
    assert checkout.total_price == 1000.0


def test_create_checkout_without_cart(client, clean_tables):
    # Given

    # When
    response = client.post("/checkout/")

    # Then
    assert response.status_code == 404
