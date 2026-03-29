import pytest

from app.models.checkout import Checkout, CheckoutStatus
from app.repositories.checkout_repository import CheckoutRepository
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
def clean_checkout_table(db_session):
    # Given
    db_session.query(Checkout).delete()
    db_session.commit()

    yield

    db_session.query(Checkout).delete()
    db_session.commit()


@pytest.fixture
def seeded_checkouts(db_session, clean_checkout_table):
    # Given
    checkouts = [
        Checkout(user_id=1, currency="PLN", status="PENDING", total_price=100.0, payment_method_id=1),
        Checkout(user_id=2, currency="EUR", status="COMPLETED", total_price=200.0, payment_method_id=2),
        Checkout(user_id=3, currency="USD", status="PENDING", total_price=300.0, payment_method_id=3),
    ]

    for checkout in checkouts:
        db_session.add(checkout)
    db_session.commit()

    return checkouts


def test_get_checkout_by_id(db_session, seeded_checkouts):
    # Given
    repo = CheckoutRepository(db_session)
    checkout_id = seeded_checkouts[0].id

    # When
    result = repo.get_checkout_by_id(checkout_id)

    # Then
    assert result is not None
    assert result.user_id == 1


def test_get_cart_by_user_id_and_status(db_session, seeded_checkouts):
    # Given
    repo = CheckoutRepository(db_session)

    # When
    result = repo.get_cart_by_user_id_and_status(2, CheckoutStatus.COMPLETED)

    # Then
    assert result is not None
    assert result.currency == "EUR"
    assert result.status == "COMPLETED"


def test_get_checkouts_paginated(db_session, seeded_checkouts):
    # Given
    repo = CheckoutRepository(db_session)

    # When
    items, total = repo.get_checkouts_paginated(page=1, size=2)

    # Then
    assert total == 3
    assert len(items) == 2
