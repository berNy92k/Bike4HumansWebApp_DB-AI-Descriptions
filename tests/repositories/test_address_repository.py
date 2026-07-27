import pytest

from app.models.user import Address
from app.repositories.address_repository import AddressRepository
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
def clean_address_table(db_session):
    # Given
    db_session.query(Address).delete()
    db_session.commit()

    yield

    db_session.query(Address).delete()
    db_session.commit()


@pytest.fixture
def seeded_address(db_session, clean_address_table):
    # Given
    address = Address(address_line_1="Street 1", city="Warszawa", postal_code="00-001",
                       country_code="PL", state_province="Mazowieckie")
    db_session.add(address)
    db_session.commit()

    return address


def test_get_address_by_id_found(db_session, seeded_address):
    # Given
    repo = AddressRepository(db_session)

    # When
    result = repo.get_address_by_id(seeded_address.id)

    # Then
    assert result is not None
    assert result.city == "Warszawa"


def test_get_address_by_id_not_found(db_session, clean_address_table):
    # Given
    repo = AddressRepository(db_session)

    # When
    result = repo.get_address_by_id(999999)

    # Then
    assert result is None


def test_create_or_update_inserts_new_address(db_session, clean_address_table):
    # Given
    repo = AddressRepository(db_session)
    address = Address(address_line_1="Street 5", city="Gdansk", postal_code="80-001",
                       country_code="PL", state_province="Pomorskie")

    # When
    repo.create_or_update(address)

    # Then
    assert address.id is not None
    stored = repo.get_address_by_id(address.id)
    assert stored.city == "Gdansk"


def test_create_or_update_updates_existing_address_in_place(db_session, seeded_address):
    # Given
    repo = AddressRepository(db_session)
    seeded_address.city = "Poznan"

    # When
    repo.create_or_update(seeded_address)

    # Then
    db_session.expire_all()
    stored = repo.get_address_by_id(seeded_address.id)
    assert stored.city == "Poznan"
    assert db_session.query(Address).count() == 1
