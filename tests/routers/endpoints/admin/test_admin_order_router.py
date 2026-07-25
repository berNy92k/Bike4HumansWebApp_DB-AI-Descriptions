from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.order import Order, OrderItem, OrderStatus
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
    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(Bike).delete()
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.execute(role_permission.delete())
    db_session.query(Permission).delete()
    db_session.query(Role).delete()
    db_session.commit()

    yield

    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(Bike).delete()
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
    bike = Bike(name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1, brand_id=1)
    db_session.add(bike)
    db_session.flush()

    order = Order(order_id="ORD00000001", user_id=1, currency="PLN", status=OrderStatus.PENDING.name,
                  total_price=100.0, payment_method_id=1)
    order.items.append(OrderItem(bike_id=bike.id, quantity=1))

    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    db_session.add(order)
    db_session.commit()

    return order


def test_update_order_status(client, seeded_data, db_session):
    # Given
    order_id = seeded_data.id

    # When
    response = client.put(f"/admin/orders/{order_id}", params={"status": "delivery"})

    # Then
    assert response.status_code == 200
    db_session.expire_all()
    updated = db_session.query(Order).filter(Order.id == order_id).first()
    assert updated.status == OrderStatus.DELIVERY.name


def test_delete_order(client, seeded_data, db_session):
    # Given
    order_id = seeded_data.id

    # When
    response = client.delete(f"/admin/orders/{order_id}")

    # Then
    assert response.status_code == 200
    assert db_session.query(Order).filter(Order.id == order_id).first() is None


def test_delete_order_not_found(client, seeded_data):
    # Given

    # When
    response = client.delete("/admin/orders/999999")

    # Then
    assert response.status_code == 404


def test_generate_order_summary(client, seeded_data):
    # Given
    order_id = seeded_data.id

    with patch(
        "app.services.admin.admin_order_service.OrderSummaryAiService.generate_summary",
        return_value="Zamówienie zawiera 1 rower Trek Marlin 7 o wartości 100.0 PLN, status: oczekujące.",
    ):
        # When
        response = client.post(f"/admin/orders/{order_id}/ai-summary")

    # Then
    assert response.status_code == 201
    assert "Trek Marlin 7" in response.json()["summary"]


def test_generate_order_summary_not_found(client, seeded_data):
    # Given

    # When
    response = client.post("/admin/orders/999999/ai-summary")

    # Then
    assert response.status_code == 404
