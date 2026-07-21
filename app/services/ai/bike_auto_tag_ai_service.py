import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.schemas.admin.bike.admin_bike_auto_tag_request_dto import BikeAutoTagRequestDto
from app.schemas.admin.bike.admin_bike_auto_tag_response_dto import BikeAutoTagResponseDto

load_dotenv()

SYSTEM_PROMPT = """Jesteś ekspertem od rowerów pracującym dla sklepu rowerowego. Na podstawie nazwy i opisu
roweru określ jego cechy, wybierając wyłącznie spośród wartości dozwolonych przez podany schemat.

Jeśli opis nie zawiera wystarczających informacji, aby pewnie określić dane pole, zwróć dla niego null -
nie zgaduj i nie zmyślaj cech, których opis nie sugeruje."""


class BikeAutoTagAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_tags(self, bike: BikeAutoTagRequestDto) -> BikeAutoTagResponseDto:
        if not self._api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured.",
            )

        client = OpenAI(api_key=self._api_key)

        try:
            completion = client.chat.completions.parse(
                model=self._model,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Nazwa: {bike.name}\nOpis: {bike.description}"},
                ],
                response_format=BikeAutoTagResponseDto,
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate tags from AI provider.",
            ) from exc

        parsed = completion.choices[0].message.parsed
        if parsed is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an unparsable response.",
            )

        return parsed
