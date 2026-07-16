import pytest
from fastapi import HTTPException

from app.models.bike import Bike
from app.models.cart import Cart, CartItem, CartStatus
from app.models.checkout import Checkout, CheckoutItem
from app.services.front.checkout_service import CheckoutService
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
    cart.items.append(CartItem(bike_id=bike.id, quantity=2))
    db_session.add(cart)
    db_session.commit()

    return cart


def test_create_checkout(db_session, seeded_pending_cart):
    # Given
    service = CheckoutService(db_session)

    # When
    service.create_checkout(user_id=1)

    # Then
    checkout = service.get_cart_by_user_id_and_status_pending(1)
    assert checkout.total_price == 2000.0
    assert len(checkout.items) == 1
    assert checkout.items[0].quantity == 2

    db_session.expire_all()
    cart = db_session.get(Cart, seeded_pending_cart.id)
    assert cart.status == CartStatus.COMPLETED.name


def test_create_checkout_without_cart(db_session, clean_tables):
    # Given
    service = CheckoutService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.create_checkout(user_id=99)

    assert exc.value.status_code == 404


def test_get_cart_by_user_id_and_status_pending_not_found(db_session, clean_tables):
    # Given
    service = CheckoutService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_cart_by_user_id_and_status_pending(1)

    assert exc.value.status_code == 404


def test_get_cart_by_user_id_and_status_completed_not_found_for_pending_checkout(db_session, seeded_pending_cart):
    # Given
    service = CheckoutService(db_session)
    service.create_checkout(user_id=1)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_cart_by_user_id_and_status_completed(1)

    assert exc.value.status_code == 404
