import pytest

from app.models.payment_method import PaymentMethod
from app.repositories.payment_methods_repository import PaymentMethodRepository
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
def clean_payment_method_table(db_session):
    # Given
    db_session.query(PaymentMethod).delete()
    db_session.commit()

    yield

    db_session.query(PaymentMethod).delete()
    db_session.commit()


@pytest.fixture
def seeded_payment_methods(db_session, clean_payment_method_table):
    # Given
    methods = [
        PaymentMethod(name="Karta", price=2.5),
        PaymentMethod(name="BLIK", price=1.5),
        PaymentMethod(name="Przelew", price=0.0),
    ]

    for method in methods:
        db_session.add(method)
    db_session.commit()

    return methods


def test_get_methods(db_session, seeded_payment_methods):
    # Given
    repo = PaymentMethodRepository(db_session)

    # When
    result = repo.get_methods()

    # Then
    assert len(result) == 3


def test_get_method_by_id(db_session, seeded_payment_methods):
    # Given
    repo = PaymentMethodRepository(db_session)
    method_id = seeded_payment_methods[0].id

    # When
    result = repo.get_method_by_id(method_id)

    # Then
    assert result is not None
    assert result.name == "Karta"
