from app.models.manufacturer import Manufacturer


def test_manufacturer_table_name():
    assert Manufacturer.__tablename__ == "manufacturer"


def test_manufacturer_has_expected_columns():
    columns = Manufacturer.__table__.columns

    assert "name" in columns
    assert "description" in columns
    assert "image_url" in columns
    assert "created_by" in columns


def test_manufacturer_required_columns_are_not_nullable():
    columns = Manufacturer.__table__.columns

    assert columns["name"].nullable is False
    assert columns["created_by"].nullable is False


def test_manufacturer_can_be_created():
    manufacturer = Manufacturer(
        name="Trek",
        description="Producent rowerów",
        image_url="https://example.com/trek.png",
        created_by=1,
    )

    assert manufacturer.name == "Trek"
    assert manufacturer.description == "Producent rowerów"
    assert manufacturer.image_url == "https://example.com/trek.png"
    assert manufacturer.created_by == 1
