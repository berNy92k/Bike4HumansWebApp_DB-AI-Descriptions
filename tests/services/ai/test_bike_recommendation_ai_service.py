import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.models.bike import Bike
from app.services.ai.bike_recommendation_ai_service import BikeRecommendationAiService


def _make_bike(**overrides):
    defaults = dict(name="Trek Marlin 7", price=3999.99, stock_quantity=5, created_by=1, brand_id=1)
    defaults.update(overrides)
    return Bike(**defaults)


def test_generate_recommendation_note_returns_trimmed_ai_content():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeRecommendationAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="  Warto rozważyć te opcje.  "))
    ]

    with patch("app.services.ai.bike_recommendation_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_recommendation_note(_make_bike(), [_make_bike(name="Giant Talon 1")])

    # Then
    assert result == "Warto rozważyć te opcje."


def test_generate_recommendation_note_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = BikeRecommendationAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_recommendation_note(_make_bike(), [_make_bike()])

    assert exc.value.status_code == 500


def test_generate_recommendation_note_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeRecommendationAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("boom")

    with patch("app.services.ai.bike_recommendation_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_recommendation_note(_make_bike(), [_make_bike()])

    assert exc.value.status_code == 502


def test_build_user_prompt_includes_current_and_similar_bikes():
    # Given
    current = _make_bike(bike_type="MOUNTAIN", usage="TRAIL")
    similar = _make_bike(name="Giant Talon 1", bike_type="MOUNTAIN")

    # When
    prompt = BikeRecommendationAiService._build_user_prompt(current, [similar])

    # Then
    assert "Typ roweru: MOUNTAIN" in prompt
    assert "typ: MOUNTAIN" in prompt
