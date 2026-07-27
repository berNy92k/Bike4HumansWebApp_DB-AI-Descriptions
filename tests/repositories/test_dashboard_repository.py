from datetime import datetime

import pytest

from app.models.bike import Bike
from app.models.manufacturer import Manufacturer
from app.models.order import Order, OrderItem
from app.repositories.dashboard_repository import DashboardRepository
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
def clean_tables(db_session):
    # Given
    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(Bike).delete()
    db_session.query(Manufacturer).delete()
    db_session.commit()

    yield

    db_session.query(OrderItem).delete()
    db_session.query(Order).delete()
    db_session.query(Bike).delete()
    db_session.query(Manufacturer).delete()
    db_session.commit()


@pytest.fixture
def seeded_data(db_session, clean_tables):
    # Given
    manufacturer_with_bikes = Manufacturer(name="Trek", description="Bike brand", created_by=1)
    manufacturer_without_bikes = Manufacturer(name="Empty Brand", description="No bikes yet", created_by=1)
    db_session.add(manufacturer_with_bikes)
    db_session.add(manufacturer_without_bikes)
    db_session.commit()

    complete_bike = Bike(
        name="Trek Marlin 7", price=100.0, stock_quantity=5, created_by=1,
        brand_id=manufacturer_with_bikes.id, image_url="/static/marlin.png",
        description="Solidny rower górski.", bike_type="MOUNTAIN", frame_material="ALUMINIUM",
    )
    incomplete_bike = Bike(
        name="Trek FX 3", price=50.0, stock_quantity=2, created_by=1,
        brand_id=manufacturer_with_bikes.id,
    )
    db_session.add(complete_bike)
    db_session.add(incomplete_bike)
    db_session.commit()

    orders = [
        Order(order_id="ORD00000001", user_id=1, currency="PLN", status="COMPLETED",
              total_price=300.0, payment_method_id=1, created_at=datetime(2026, 1, 15)),
        Order(order_id="ORD00000002", user_id=2, currency="PLN", status="DELIVERY",
              total_price=200.0, payment_method_id=1, created_at=datetime(2026, 2, 10)),
        Order(order_id="ORD00000003", user_id=3, currency="PLN", status="CANCELED",
              total_price=999.0, payment_method_id=1, created_at=datetime(2026, 2, 12)),
        Order(order_id="ORD00000004", user_id=1, currency="PLN", status="PENDING",
              total_price=100.0, payment_method_id=1, created_at=datetime(2026, 2, 14)),
    ]
    for order in orders:
        db_session.add(order)
    db_session.commit()

    db_session.add(OrderItem(order_id=orders[0].id, bike_id=complete_bike.id, quantity=3))
    db_session.add(OrderItem(order_id=orders[1].id, bike_id=complete_bike.id, quantity=1))
    db_session.add(OrderItem(order_id=orders[1].id, bike_id=incomplete_bike.id, quantity=2))
    db_session.commit()

    return {
        "manufacturer_with_bikes": manufacturer_with_bikes,
        "manufacturer_without_bikes": manufacturer_without_bikes,
        "complete_bike": complete_bike,
        "incomplete_bike": incomplete_bike,
        "orders": orders,
    }


def test_get_bikes_count(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    result = repo.get_bikes_count()

    # Then
    assert result == 2


def test_get_manufacturers_count(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    result = repo.get_manufacturers_count()

    # Then
    assert result == 2


def test_get_orders_count(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    result = repo.get_orders_count()

    # Then
    assert result == 4


def test_get_realized_revenue_stats_only_counts_completed_and_delivery(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    total_revenue, count = repo.get_realized_revenue_stats()

    # Then
    assert total_revenue == 500.0
    assert count == 2


def test_get_orders_by_status(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    result = dict(repo.get_orders_by_status())

    # Then
    assert result == {"COMPLETED": 1, "DELIVERY": 1, "CANCELED": 1, "PENDING": 1}


def test_get_revenue_by_month(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    result = dict(repo.get_revenue_by_month(months=12))

    # Then
    assert result["2026-01"] == 300.0
    assert result["2026-02"] == 200.0


def test_get_top_selling_bikes(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)
    complete_bike = seeded_data["complete_bike"]
    incomplete_bike = seeded_data["incomplete_bike"]

    # When
    result = repo.get_top_selling_bikes(limit=5)

    # Then
    by_bike_id = {row[0]: row for row in result}
    assert by_bike_id[complete_bike.id][2] == 4  # 3 (COMPLETED order) + 1 (DELIVERY order)
    assert by_bike_id[incomplete_bike.id][2] == 2  # 2 (DELIVERY order)


def test_get_catalog_health(db_session, seeded_data):
    # Given
    repo = DashboardRepository(db_session)

    # When
    result = repo.get_catalog_health()

    # Then
    assert result["bikes_with_image_pct"] == 50.0
    assert result["bikes_with_description_pct"] == 50.0
    assert result["bikes_complete_pct"] == 50.0
    assert result["manufacturers_with_bikes_pct"] == 50.0
