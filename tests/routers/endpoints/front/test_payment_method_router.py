import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.payment_method import PaymentMethod
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
    return TestClient(app)


@pytest.fixture
def clean_payment_methods_table(db_session):
    # Given
    db_session.query(PaymentMethod).delete()
    db_session.commit()

    yield

    db_session.query(PaymentMethod).delete()
    db_session.commit()


@pytest.fixture
def seeded_payment_methods(db_session, clean_payment_methods_table):
    # Given
    methods = [
        PaymentMethod(name="Card", price=0.0),
        PaymentMethod(name="BLIK", price=0.0),
    ]
    for method in methods:
        db_session.add(method)
    db_session.commit()

    return methods


def test_find_payment_methods(client, seeded_payment_methods):
    # Given

    # When
    response = client.get("/payment-methods/")

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_find_payment_method_by_id(client, seeded_payment_methods):
    # Given
    method_id = seeded_payment_methods[0].id

    # When
    response = client.get(f"/payment-methods/{method_id}")

    # Then
    assert response.status_code == 200
    assert response.json()["name"] == "Card"


def test_find_payment_method_by_id_not_found(client, seeded_payment_methods):
    # Given

    # When
    response = client.get("/payment-methods/999999")

    # Then
    assert response.status_code == 404
