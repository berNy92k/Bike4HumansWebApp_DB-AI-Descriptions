import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.models.cart import Cart, CartItem, CartStatus
from app.services.front.cart_service import CartService
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


def test_add_item_to_cart_creates_new_cart(db_session, seeded_bike):
    # Given
    service = CartService(db_session)

    # When
    service.add_item_to_cart(user_id=1, bike_id=seeded_bike.id)

    # Then
    cart = service.get_cart_by_user_id_and_pending_status(1)
    assert len(cart.items) == 1
    assert cart.items[0].bike_id == seeded_bike.id
    assert cart.items[0].quantity == 1


def test_add_item_to_cart_increments_existing_item_quantity(db_session, seeded_bike):
    # Given
    service = CartService(db_session)
    service.add_item_to_cart(user_id=1, bike_id=seeded_bike.id)

    # When
    service.add_item_to_cart(user_id=1, bike_id=seeded_bike.id)

    # Then
    cart = service.get_cart_by_user_id_and_pending_status(1)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 2


def test_add_item_to_cart_bike_not_found(db_session, seeded_bike):
    # Given
    service = CartService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.add_item_to_cart(user_id=1, bike_id=999999)

    assert exc.value.status_code == 404


def test_get_cart_by_user_id_and_pending_status_not_found(db_session, seeded_bike):
    # Given
    service = CartService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_cart_by_user_id_and_pending_status(1)

    assert exc.value.status_code == 404


def test_get_cart_by_user_id_and_pending_status_ignores_completed_cart(db_session, seeded_bike):
    # Given
    completed_cart = Cart(user_id=1, currency="PLN", status=CartStatus.COMPLETED.name)
    db_session.add(completed_cart)
    db_session.commit()
    service = CartService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_cart_by_user_id_and_pending_status(1)

    assert exc.value.status_code == 404
