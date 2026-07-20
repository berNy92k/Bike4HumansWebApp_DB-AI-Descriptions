import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from openai import OpenAIError

from app.schemas.admin.manufacturers.admin_manufacturer_ai_description_request_dto import ManufacturerAiDescriptionRequestDto
from app.services.ai.manufacturer_description_ai_service import ManufacturerDescriptionAiService


def _make_request_dto(**overrides):
    defaults = dict(name="Trek")
    defaults.update(overrides)
    return ManufacturerAiDescriptionRequestDto(**defaults)


def test_generate_description_returns_trimmed_ai_content():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = ManufacturerDescriptionAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="  Świetna marka rowerowa.  "))
    ]

    with patch("app.services.ai.manufacturer_description_ai_service.OpenAI", return_value=mock_client):
        # When
        result = service.generate_description(_make_request_dto())

    # Then
    assert result == "Świetna marka rowerowa."


def test_generate_description_missing_api_key_raises_500():
    # Given
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("OPENAI_API_KEY", None)
        service = ManufacturerDescriptionAiService()

        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_description(_make_request_dto())

    assert exc.value.status_code == 500


def test_generate_description_provider_error_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = ManufacturerDescriptionAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("boom")

    with patch("app.services.ai.manufacturer_description_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_description(_make_request_dto())

    assert exc.value.status_code == 502


def test_generate_description_empty_ai_content_raises_502():
    # Given
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        service = ManufacturerDescriptionAiService()

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [MagicMock(message=MagicMock(content=None))]

    with patch("app.services.ai.manufacturer_description_ai_service.OpenAI", return_value=mock_client):
        # When / Then
        with pytest.raises(HTTPException) as exc:
            service.generate_description(_make_request_dto())

    assert exc.value.status_code == 502


def test_build_user_prompt_only_includes_provided_fields():
    # Given
    dto = _make_request_dto(description=None)

    # When
    prompt = ManufacturerDescriptionAiService._build_user_prompt(dto)

    # Then
    assert "Nazwa marki: Trek" in prompt
    assert "Istniejący opis manualny" not in prompt
