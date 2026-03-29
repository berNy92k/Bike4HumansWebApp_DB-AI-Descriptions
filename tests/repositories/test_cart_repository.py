import pytest

from app.models.cart import Cart, CartStatus
from app.repositories.cart_repository import CartRepository
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
def clean_cart_table(db_session):
    # Given
    db_session.query(Cart).delete()
    db_session.commit()

    yield

    db_session.query(Cart).delete()
    db_session.commit()


@pytest.fixture
def seeded_carts(db_session, clean_cart_table):
    # Given
    carts = [
        Cart(user_id=1, currency="PLN", status=CartStatus.PENDING.name),
        Cart(user_id=2, currency="EUR", status=CartStatus.COMPLETED.name),
        Cart(user_id=3, currency="USD", status=CartStatus.PENDING.name),
    ]

    for cart in carts:
        db_session.add(cart)
    db_session.commit()

    return carts


def test_get_cart_by_id(db_session, seeded_carts):
    # Given
    repo = CartRepository(db_session)
    cart_id = seeded_carts[0].id

    # When
    result = repo.get_cart_by_id(cart_id)

    # Then
    assert result is not None
    assert result.user_id == 1


def test_get_cart_by_user_id(db_session, seeded_carts):
    # Given
    repo = CartRepository(db_session)

    # When
    result = repo.get_cart_by_user_id(2)

    # Then
    assert result is not None
    assert result.currency == "EUR"


def test_get_cart_by_user_id_and_status(db_session, seeded_carts):
    # Given
    repo = CartRepository(db_session)

    # When
    result = repo.get_cart_by_user_id_and_status(1, CartStatus.PENDING)

    # Then
    assert result is not None
    assert result.user_id == 1
    assert result.status == CartStatus.PENDING.name


def test_get_carts_paginated(db_session, seeded_carts):
    # Given
    repo = CartRepository(db_session)

    # When
    items, total = repo.get_carts_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2
