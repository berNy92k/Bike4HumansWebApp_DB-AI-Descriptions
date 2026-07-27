import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.models.manufacturer import Manufacturer
from app.models.order import Order, OrderItem
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
    db_session.query(Manufacturer).delete()
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
    db_session.query(Manufacturer).delete()
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
        id=1, address_line_1="Street 1", city="Warszawa", postal_code="00-001",
        country_code="PL", state_province="Mazowieckie",
    )
    user = User(
        id=1, username="admin", email="admin@example.com", name="Admin", surname="One",
        hashed_password="hash", is_active=True, email_verified=True, role_id=1, address_id=1,
    )
    manufacturer = Manufacturer(name="Trek", description="Bike brand", created_by=1)
    db_session.add(role)
    db_session.add(address)
    db_session.add(user)
    db_session.add(manufacturer)
    db_session.commit()

    bike = Bike(
        name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1, brand_id=manufacturer.id,
        image_url="/static/marlin.png", description="Solidny rower górski.",
        bike_type="MOUNTAIN", frame_material="ALUMINIUM",
    )
    db_session.add(bike)
    db_session.commit()

    order = Order(order_id="ORD00000001", user_id=user.id, currency="PLN", status="COMPLETED",
                  total_price=100.0, payment_method_id=1)
    db_session.add(order)
    db_session.commit()
    db_session.add(OrderItem(order_id=order.id, bike_id=bike.id, quantity=1))
    db_session.commit()

    return {"manufacturer": manufacturer, "bike": bike, "order": order}


def test_get_dashboard_stats(client, seeded_data):
    # Given

    # When
    response = client.get("/admin/dashboard/stats")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["bikes_count"] == 1
    assert data["manufacturers_count"] == 1
    assert data["orders_count"] == 1
    assert data["orders_total_revenue"] == 100.0
    assert data["average_order_value"] == 100.0
    assert data["orders_by_status"] == [{"status": "COMPLETED", "count": 1}]
    assert data["top_bikes"][0]["name"] == "Trek Marlin 7"
    assert data["catalog_health"]["bikes_complete_pct"] == 100.0


def test_get_dashboard_stats_requires_admin_permission(db_session):
    # Given
    app.dependency_overrides[get_current_user] = lambda: {"user_id": 999, "role_id": 999}
    client = TestClient(app)

    # When
    response = client.get("/admin/dashboard/stats")

    # Then
    assert response.status_code == 403
    app.dependency_overrides.pop(get_current_user, None)
