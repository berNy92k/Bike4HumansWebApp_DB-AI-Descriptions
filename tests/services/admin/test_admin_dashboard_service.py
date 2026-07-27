from unittest.mock import MagicMock

from app.services.admin.admin_dashboard_service import AdminDashboardService


def test_get_dashboard_stats_assembles_repository_data():
    # Given
    mock_repo = MagicMock()
    mock_repo.get_bikes_count.return_value = 10
    mock_repo.get_manufacturers_count.return_value = 3
    mock_repo.get_users_count.return_value = 5
    mock_repo.get_roles_count.return_value = 4
    mock_repo.get_orders_count.return_value = 7
    mock_repo.get_realized_revenue_stats.return_value = (1000.0, 4)
    mock_repo.get_orders_by_status.return_value = [("COMPLETED", 4), ("PENDING", 3)]
    mock_repo.get_revenue_by_month.return_value = [("2026-01", 500.0), ("2026-02", 500.0)]
    mock_repo.get_top_selling_bikes.return_value = [(1, "Trek Marlin 7", 3, 900.0)]
    mock_repo.get_catalog_health.return_value = {
        "bikes_with_image_pct": 80.0,
        "bikes_with_description_pct": 90.0,
        "bikes_complete_pct": 70.0,
        "manufacturers_with_bikes_pct": 100.0,
    }

    service = AdminDashboardService.__new__(AdminDashboardService)
    service.dashboard_repository = mock_repo

    # When
    result = service.get_dashboard_stats()

    # Then
    assert result.bikes_count == 10
    assert result.orders_total_revenue == 1000.0
    assert result.average_order_value == 250.0
    assert [s.model_dump() for s in result.orders_by_status] == [
        {"status": "COMPLETED", "count": 4},
        {"status": "PENDING", "count": 3},
    ]
    assert result.revenue_by_month[0].month == "2026-01"
    assert result.top_bikes[0].name == "Trek Marlin 7"
    assert result.catalog_health.bikes_with_image_pct == 80.0


def test_get_dashboard_stats_zero_orders_avoids_division_by_zero():
    # Given
    mock_repo = MagicMock()
    mock_repo.get_bikes_count.return_value = 0
    mock_repo.get_manufacturers_count.return_value = 0
    mock_repo.get_users_count.return_value = 0
    mock_repo.get_roles_count.return_value = 0
    mock_repo.get_orders_count.return_value = 0
    mock_repo.get_realized_revenue_stats.return_value = (0.0, 0)
    mock_repo.get_orders_by_status.return_value = []
    mock_repo.get_revenue_by_month.return_value = []
    mock_repo.get_top_selling_bikes.return_value = []
    mock_repo.get_catalog_health.return_value = {
        "bikes_with_image_pct": 0.0,
        "bikes_with_description_pct": 0.0,
        "bikes_complete_pct": 0.0,
        "manufacturers_with_bikes_pct": 0.0,
    }

    service = AdminDashboardService.__new__(AdminDashboardService)
    service.dashboard_repository = mock_repo

    # When
    result = service.get_dashboard_stats()

    # Then
    assert result.average_order_value == 0.0
