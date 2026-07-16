import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.schemas.admin.bike.admin_bike_ai_description_request_dto import BikeAiDescriptionRequestDto
from app.services.ai.bike_description_ai_service import BikeDescriptionAiService


def _make_request_dto(**overrides):
    defaults = dict(name="Trek Marlin 7", brand_id=1)
    defaults.update(overrides)
    return BikeAiDescriptionRequestDto(**defaults)


def test_generate_description_returns_trimmed_ai_content():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeDescriptionAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="  Świetny rower miejski.  "))
    ]

    with patch("app.services.ai.bike_description_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_description(_make_request_dto())

    # Then
    assert result == "Świetny rower miejski."


def test_generate_description_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = BikeDescriptionAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_description(_make_request_dto())

    assert exc.value.status_code == 500


def test_generate_description_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeDescriptionAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("boom")

    with patch("app.services.ai.bike_description_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_description(_make_request_dto())

    assert exc.value.status_code == 502


def test_generate_description_empty_ai_content_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = BikeDescriptionAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [MagicMock(message=MagicMock(content=None))]

    with patch("app.services.ai.bike_description_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_description(_make_request_dto())

    assert exc.value.status_code == 502


def test_build_user_prompt_only_includes_provided_fields():
    # Given
    dto = _make_request_dto(bike_type="MOUNTAIN", description=None)

    # When
    prompt = BikeDescriptionAiService._build_user_prompt(dto)

    # Then
    assert "Typ roweru: MOUNTAIN" in prompt
    assert "Istniejący opis manualny" not in prompt
