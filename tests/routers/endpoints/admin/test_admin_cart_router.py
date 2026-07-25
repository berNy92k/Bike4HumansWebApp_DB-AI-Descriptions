from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.cart import Cart, CartStatus
from app.models.permission import Permission, PermissionCode, role_permission
from app.models.role import Role
from app.models.user import User, Address
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
    app.dependency_overrides[get_current_user] = lambda: {"user_id": 1, "role_id": 1}
    client = TestClient(app)

    yield client

    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(Cart).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(Cart).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_data(db_session, clean_tables):
    # Given
    admin_panel_access = Permission(code=PermissionCode.ADMIN_PANEL_ACCESS)
    db_session.add(admin_panel_access)
    db_session.flush()

    role = Role(id=1, name="Admin", description="Admin role", permissions=[admin_panel_access])
    address = Address(
        id=1,
        address_line_1="Street 1",
        city="Warszawa",
        postal_code="00-001",
        country_code="PL",
        state_province="Mazowieckie",
    )
    user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        name="Admin",
        surname="One",
        hashed_password="hash",
        is_active=True,
        email_verified=True,
        role_id=1,
        address_id=1,
    )
    cart = Cart(user_id=1, currency="PLN", status=CartStatus.PENDING.name)

    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    db_session.add(cart)
    db_session.commit()

    return cart


def test_delete_cart(client, seeded_data, db_session):
    # Given
    cart_id = seeded_data.id

    # When
    response = client.delete(f"/admin/carts/{cart_id}")

    # Then
    assert response.status_code == 200
    assert db_session.query(Cart).filter(Cart.id == cart_id).first() is None


def test_delete_cart_not_found(client, seeded_data):
    # Given

    # When
    response = client.delete("/admin/carts/999999")

    # Then
    assert response.status_code == 404


def test_generate_cart_summary(client, seeded_data):
    # Given
    cart_id = seeded_data.id

    with patch(
        "app.services.admin.admin_cart_service.CartSummaryAiService.generate_summary",
        return_value="Koszyk jest pusty, status: oczekujący.",
    ):
        # When
        response = client.post(f"/admin/carts/{cart_id}/ai-summary")

    # Then
    assert response.status_code == 201
    assert "Koszyk" in response.json()["summary"]


def test_generate_cart_summary_not_found(client, seeded_data):
    # Given

    # When
    response = client.post("/admin/carts/999999/ai-summary")

    # Then
    assert response.status_code == 404
