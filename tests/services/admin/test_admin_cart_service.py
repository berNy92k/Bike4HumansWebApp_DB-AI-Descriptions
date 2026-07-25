from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.cart import Cart, CartStatus
from app.services.admin.admin_cart_service import AdminCartService
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
def clean_carts_table(db_session):
    # Given
    db_session.query(Cart).delete()
    db_session.commit()

    yield

    db_session.query(Cart).delete()
    db_session.commit()


@pytest.fixture
def seeded_cart(db_session, clean_carts_table):
    # Given
    cart = Cart(user_id=1, currency="PLN", status=CartStatus.PENDING.name)
    db_session.add(cart)
    db_session.commit()

    return cart


def test_delete_cart_by_id_not_found(db_session):
    # Given
    service = AdminCartService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.delete_cart_by_id(999999)

    assert exc.value.status_code == 404


def test_generate_cart_summary_caches_result(db_session, seeded_cart):
    # Given
    mock_ai_summary_service = MagicMock()
    mock_ai_summary_service.generate_summary.return_value = "Podsumowanie koszyka."
    service = AdminCartService(db_session, ai_summary_service=mock_ai_summary_service)

    # When
    service.generate_cart_summary(seeded_cart.id)
    result = service.generate_cart_summary(seeded_cart.id)

    # Then
    assert result.summary == "Podsumowanie koszyka."
    mock_ai_summary_service.generate_summary.assert_called_once()

    db_session.expire_all()
    cached = db_session.query(Cart).filter(Cart.id == seeded_cart.id).first()
    assert cached.ai_summary == "Podsumowanie koszyka."
    assert cached.ai_summary_generated_at is not None


def test_generate_cart_summary_not_found(db_session):
    # Given
    service = AdminCartService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.generate_cart_summary(999999)

    assert exc.value.status_code == 404
