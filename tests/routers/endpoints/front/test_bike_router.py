from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bike import Bike
from app.schemas.front.bike.bike_search_filters_response_dto import BikeSearchFiltersResponseDto
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


@pytest.fixture
def clean_bikes_table(db_session):
    # Given
    db_session.query(Bike).delete()
    db_session.commit()

    yield

    db_session.query(Bike).delete()
    db_session.commit()


@pytest.fixture
def seeded_bikes(db_session, clean_bikes_table):
    # Given
    bikes = [
        Bike(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1, bike_type="MOUNTAIN"),
        Bike(name="Giant Talon 1", price=3499.00, stock_quantity=3, created_by=1, brand_id=1, bike_type="MOUNTAIN"),
    ]
    for bike in bikes:
        db_session.add(bike)
    db_session.commit()

    return bikes


def test_get_similar_bikes_recommendation(client, seeded_bikes):
    # Given
    bike_id = seeded_bikes[0].id

    with patch(
        "app.services.front.bike_service.BikeRecommendationAiService.generate_recommendation_note",
        return_value="Warto rozważyć te opcje.",
    ):
        # When
        response = client.post(f"/bikes/{bike_id}/ai-similar-bikes")

    # Then
    assert response.status_code == 201
    data = response.json()
    assert data["note"] == "Warto rozważyć te opcje."
    assert len(data["bikes"]) == 1
    assert data["bikes"][0]["name"] == "Giant Talon 1"


def test_get_similar_bikes_recommendation_bike_not_found(client, seeded_bikes):
    # Given

    # When
    response = client.post("/bikes/999999/ai-similar-bikes")

    # Then
    assert response.status_code == 404


def test_generate_search_filters(client, seeded_bikes):
    # Given
    payload = {"query": "szukam czegoś do miasta do 3000 zł"}
    ai_response = BikeSearchFiltersResponseDto(bike_type="CITY", price_max=3000)

    with patch(
        "app.services.front.bike_service.BikeSearchAiService.generate_filters",
        return_value=ai_response,
    ):
        # When
        response = client.post("/bikes/ai-search", json=payload)

    # Then
    assert response.status_code == 201
    assert response.json() == {
        "bike_type": "CITY", "usage": None, "target_user": None, "price_min": None, "price_max": 3000
    }


def test_generate_search_filters_requires_query(client, seeded_bikes):
    # Given

    # When
    response = client.post("/bikes/ai-search", json={"query": ""})

    # Then
    assert response.status_code == 422
