from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.order import Order, OrderStatus
from app.models.permission import Permission, PermissionCode, role_permission
from app.models.role import Role
from app.models.user import User, Address
from app.services.auth.auth_service import generate_jwt_token
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


def _login(client: TestClient, user_id: int = 1, username: str = "admin", role_id: int = 1) -> None:
    token = generate_jwt_token(username, user_id, role_id, timedelta(minutes=20))
    client.cookies.set("access_token", token)


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(Order).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(Order).delete()
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
    order = Order(order_id="ORD00000001", user_id=1, currency="PLN", status=OrderStatus.PENDING.name,
                  total_price=100.0, payment_method_id=1)

    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    db_session.add(order)
    db_session.commit()

    return order


def test_render_orders_page_authenticated(client, seeded_data):
    # Given
    _login(client)

    # When
    response = client.get("/admin/orders/list")

    # Then
    assert response.status_code == 200
    assert "ORD00000001" in response.text


def test_render_orders_page_unauthenticated_redirects_to_login(client, seeded_data):
    # Given

    # When
    response = client.get("/admin/orders/list", follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"
