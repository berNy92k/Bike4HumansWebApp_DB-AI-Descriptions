from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.order import Order, OrderItem, OrderStatus
from app.models.payment_method import PaymentMethod
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


def _login(client: TestClient, user_id: int = 1, username: str = "john", role_id: int = 4) -> None:
    token = generate_jwt_token(username, user_id, role_id, timedelta(minutes=20))
    client.cookies.set("access_token", token)


@pytest.fixture
def clean_tables(db_session):
    # Given
    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(PaymentMethod).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(PaymentMethod).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()


@pytest.fixture
def seeded_order(db_session, clean_tables):
    # Given
    role = Role(id=4, name="user", description="User")
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
        username="john",
        email="john@example.com",
        name="John",
        surname="Doe",
        hashed_password="hash",
        is_active=True,
        email_verified=True,
        role_id=4,
        address_id=1,
    )
    method = PaymentMethod(name="Karta", price=2.5)

    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    db_session.add(method)
    db_session.flush()

    order = Order(order_id="ORD00000001", user_id=user.id, currency="PLN", status=OrderStatus.PENDING.name,
                  total_price=1000.0, payment_method_id=method.id)
    order.items.append(OrderItem(bike_id=1, quantity=1))
    db_session.add(order)
    db_session.commit()

    return order


def test_render_payment_result_authenticated(client, seeded_order):
    # Given
    _login(client)

    # When
    response = client.get("/order/details", params={"order_id": seeded_order.id})

    # Then
    assert response.status_code == 200


def test_render_payment_result_unauthenticated_redirects_to_login(client, seeded_order):
    # Given

    # When
    response = client.get("/order/details", params={"order_id": seeded_order.id}, follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"


def test_render_payment_result_order_not_found_redirects_to_login(client, seeded_order):
    # Given
    _login(client)

    # When
    response = client.get("/order/details", params={"order_id": 999999}, follow_redirects=False)

    # Then
    assert response.status_code == 303
    assert response.headers["location"] == "/auth/login"
