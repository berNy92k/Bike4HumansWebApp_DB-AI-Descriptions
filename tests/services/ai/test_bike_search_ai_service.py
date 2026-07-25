import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.schemas.front.bike.bike_search_filters_response_dto import BikeSearchFiltersResponseDto
from app.services.ai.bike_search_ai_service import BikeSearchAiService


def test_generate_filters_returns_parsed_response():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeSearchAiService()

    parsed = BikeSearchFiltersResponseDto(bike_type="CITY", price_max=3000)
    mock_client = MagicMock()
    mock_client.chat.completions.parse.return_value.choices = [MagicMock(message=MagicMock(parsed=parsed))]

    with patch("app.services.ai.bike_search_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_filters("szukam czegoś do miasta do 3000 zł")

    # Then
    assert result.bike_type == "CITY"
    assert result.price_max == 3000
    assert result.usage is None


def test_generate_filters_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = BikeSearchAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_filters("cokolwiek")

    assert exc.value.status_code == 500


def test_generate_filters_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeSearchAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.parse.side_effect = OpenAIError("boom")

    with patch("app.services.ai.bike_search_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_filters("cokolwiek")

    assert exc.value.status_code == 502


def test_generate_filters_unparsable_response_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeSearchAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.parse.return_value.choices = [MagicMock(message=MagicMock(parsed=None))]

    with patch("app.services.ai.bike_search_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_filters("cokolwiek")

    assert exc.value.status_code == 502
