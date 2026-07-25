from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.checkout import Checkout
from app.services.admin.admin_checkout_service import AdminCheckoutService
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
def clean_checkouts_table(db_session):
    # Given
    db_session.query(Checkout).delete()
    db_session.commit()

    yield

    db_session.query(Checkout).delete()
    db_session.commit()


@pytest.fixture
def seeded_checkout(db_session, clean_checkouts_table):
    # Given
    checkout = Checkout(user_id=1, currency="PLN", status="PENDING", total_price=100.0, payment_method_id=1)
    db_session.add(checkout)
    db_session.commit()

    return checkout


def test_delete_checkout_by_id_not_found(db_session):
    # Given
    service = AdminCheckoutService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.delete_checkout_by_id(999999)

    assert exc.value.status_code == 404


def test_generate_checkout_summary_caches_result(db_session, seeded_checkout):
    # Given
    mock_ai_summary_service = MagicMock()
    mock_ai_summary_service.generate_summary.return_value = "Podsumowanie checkoutu."
    service = AdminCheckoutService(db_session, ai_summary_service=mock_ai_summary_service)

    # When
    service.generate_checkout_summary(seeded_checkout.id)
    result = service.generate_checkout_summary(seeded_checkout.id)

    # Then
    assert result.summary == "Podsumowanie checkoutu."
    mock_ai_summary_service.generate_summary.assert_called_once()

    db_session.expire_all()
    cached = db_session.query(Checkout).filter(Checkout.id == seeded_checkout.id).first()
    assert cached.ai_summary == "Podsumowanie checkoutu."
    assert cached.ai_summary_generated_at is not None


def test_generate_checkout_summary_not_found(db_session):
    # Given
    service = AdminCheckoutService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.generate_checkout_summary(999999)

    assert exc.value.status_code == 404
