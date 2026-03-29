from decimal import Decimal

from app.models.bike import Bike


def test_bike_table_name():
    assert Bike.__tablename__ == "bikes"


def test_bike_has_expected_columns():
    columns = Bike.__table__.columns

    expected_columns = [
        "name",
        "description",
        "price",
        "stock_quantity",
        "image_url",
        "frame_size",
        "wheel_size",
        "color",
        "is_active",
        "created_by",
        "brand_id",
    ]

    for column_name in expected_columns:
        assert column_name in columns


def test_bike_required_columns_are_not_nullable():
    columns = Bike.__table__.columns

    assert columns["name"].nullable is False
    assert columns["price"].nullable is False
    assert columns["stock_quantity"].nullable is False
    assert columns["is_active"].nullable is False
    assert columns["created_by"].nullable is False
    assert columns["brand_id"].nullable is False


def test_bike_default_values():
    columns = Bike.__table__.columns

    assert columns["stock_quantity"].default.arg == 0
    assert columns["is_active"].default.arg is True


def test_bike_can_be_created():
    bike = Bike(
        name="Trek Marlin 7",
        description="Rower górski",
        price=Decimal("3999.99"),
        stock_quantity=5,
        image_url="https://example.com/bike.jpg",
        frame_size=19,
        wheel_size=29,
        color="Black",
        is_active=True,
        created_by=1,
        brand_id=2,
    )

    assert bike.name == "Trek Marlin 7"
    assert bike.description == "Rower górski"
    assert bike.price == Decimal("3999.99")
    assert bike.stock_quantity == 5
    assert bike.image_url == "https://example.com/bike.jpg"
    assert bike.frame_size == 19
    assert bike.wheel_size == 29
    assert bike.color == "Black"
    assert bike.is_active is True
    assert bike.created_by == 1
    assert bike.brand_id == 2
