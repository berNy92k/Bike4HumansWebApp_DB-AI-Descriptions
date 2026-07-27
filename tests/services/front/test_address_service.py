import pytest
from fastapi import HTTPException

from app.models.user import Address, User
from app.repositories.address_repository import AddressRepository
from app.schemas.front.address.address_upsert_dto import AddressUpsertDto
from app.services.front.address_service import AddressService
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
    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.commit()

    yield

    db_session.query(User).delete()
    db_session.query(Address).delete()
    db_session.commit()


@pytest.fixture
def seeded_user_with_address(db_session, clean_tables):
    # Given
    address = Address(address_line_1="Street 1", city="Warszawa", postal_code="00-001",
                       country_code="PL", state_province="Mazowieckie")
    db_session.add(address)
    db_session.commit()

    user = User(id=1, username="john", email="john@example.com", name="John", surname="Doe",
                hashed_password="hash", role_id=1, address_id=address.id)
    db_session.add(user)
    db_session.commit()

    return user, address


@pytest.fixture
def seeded_user_without_address(db_session, clean_tables):
    # Given
    user = User(id=2, username="jane", email="jane@example.com", name="Jane", surname="Doe",
                hashed_password="hash", role_id=1, address_id=None)
    db_session.add(user)
    db_session.commit()

    return user


def test_get_my_address_found(db_session, seeded_user_with_address):
    # Given
    _, address = seeded_user_with_address
    service = AddressService(db_session)

    # When
    result = service.get_my_address(1)

    # Then
    assert result.id == address.id
    assert result.city == "Warszawa"


def test_get_my_address_no_address_on_user(db_session, seeded_user_without_address):
    # Given
    service = AddressService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_my_address(2)

    assert exc.value.status_code == 404


def test_get_my_address_user_not_found(db_session, clean_tables):
    # Given
    service = AddressService(db_session)

    # When / Then
    with pytest.raises(HTTPException) as exc:
        service.get_my_address(999999)

    assert exc.value.status_code == 404


def test_save_my_address_creates_address_and_links_user(db_session, seeded_user_without_address):
    # Given
    service = AddressService(db_session)
    dto = AddressUpsertDto(address_line_1="Nowa 1", city="Krakow", postal_code="30-001",
                            country_code="PL", state_province="Malopolskie")

    # When
    result = service.save_my_address(2, dto)

    # Then
    assert result.city == "Krakow"
    db_session.expire_all()
    user = db_session.query(User).filter(User.id == 2).first()
    assert user.address_id == result.id


def test_save_my_address_updates_existing_address_in_place(db_session, seeded_user_with_address):
    # Given
    _, address = seeded_user_with_address
    service = AddressService(db_session)
    dto = AddressUpsertDto(address_line_1="Zmieniona 5", city="Poznan", postal_code="60-001",
                            country_code="PL", state_province="Wielkopolskie")

    # When
    result = service.save_my_address(1, dto)

    # Then
    assert result.id == address.id
    assert result.city == "Poznan"

    address_repository = AddressRepository(db_session)
    db_session.expire_all()
    assert db_session.query(User).filter(User.id == 1).first().address_id == address.id
    assert address_repository.get_address_by_id(address.id).city == "Poznan"
