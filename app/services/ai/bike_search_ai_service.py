import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.schemas.front.bike.bike_search_filters_response_dto import BikeSearchFiltersResponseDto

load_dotenv()

# The allowed values for bike_type/usage/target_user come from the response schema
# itself (same enums as the Bike model), so the model can only pick a value that is
# valid to filter by.
SYSTEM_PROMPT = """Jesteś asystentem wyszukiwania w sklepie rowerowym. Na podstawie opisu klienta w języku
naturalnym określ filtry wyszukiwania, wybierając wartości wyłącznie spośród dozwolonych przez podany schemat.

Jeśli klient nie wspomniał czegoś, co odpowiadałoby danemu polu, zwróć dla niego null - nie zgaduj.
Dla ceny: jeśli klient poda górny limit (np. "do 3000 zł"), ustaw price_max; jeśli poda dolny limit
(np. "od 2000 zł") lub przedział, ustaw odpowiednio price_min i/lub price_max."""


class BikeSearchAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_filters(self, query: str) -> BikeSearchFiltersResponseDto:
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
                    {"role": "user", "content": query},
                ],
                response_format=BikeSearchFiltersResponseDto,
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate search filters from AI provider.",
            ) from exc

        parsed = completion.choices[0].message.parsed
        if parsed is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an unparsable response.",
            )

        return parsed
