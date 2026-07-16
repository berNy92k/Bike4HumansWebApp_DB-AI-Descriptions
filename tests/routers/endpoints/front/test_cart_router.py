import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.cart import Cart, CartItem
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
    db_session.query(CartItem).delete()
    db_session.query(Cart).delete()
    db_session.query(Bike).delete()
    db_session.commit()

    yield

    db_session.query(CartItem).delete()
    db_session.query(Cart).delete()
    db_session.query(Bike).delete()
    db_session.commit()


@pytest.fixture
def seeded_bike(db_session, clean_tables):
    # Given
    bike = Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(bike)
    db_session.commit()

    return bike


def test_add_item_to_cart(client, seeded_bike, db_session):
    # Given
    payload = {"bike_id": seeded_bike.id}

    # When
    response = client.post("/cart/item", json=payload)

    # Then
    assert response.status_code == 204
    cart = db_session.query(Cart).filter(Cart.user_id == 1).first()
    assert cart is not None
    assert len(cart.items) == 1
    assert cart.items[0].bike_id == seeded_bike.id


def test_add_item_to_cart_bike_not_found(client, seeded_bike):
    # Given
    payload = {"bike_id": 999999}

    # When
    response = client.post("/cart/item", json=payload)

    # Then
    assert response.status_code == 404
