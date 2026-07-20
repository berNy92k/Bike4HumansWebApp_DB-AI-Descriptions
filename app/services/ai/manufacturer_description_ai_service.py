import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.schemas.admin.manufacturers.admin_manufacturer_ai_description_request_dto import ManufacturerAiDescriptionRequestDto

load_dotenv()

SYSTEM_PROMPT = """Jesteś copywriterem sklepu rowerowego. Piszesz opisy producentów (marek) rowerów po polsku.

Każdy opis MUSI się składać z dokładnie 4 akapitów, w tej kolejności, oddzielonych pojedynczą pustą linią,
bez nagłówków, list, markdownu ani emoji:
1. Chwytliwe wprowadzenie (1-2 zdania) przedstawiające markę i jej ogólny charakter/pozycjonowanie.
2. Filozofia i specjalizacja marki (2-4 zdania) - w czym się specjalizuje, jaki ma styl/podejście do produkcji
   rowerów - opieraj się tylko na podanych danych, nie zmyślaj konkretnych faktów (dat, miejsc, nagród),
   których nie podano.
3. Dla kogo jest ta marka (1-2 zdania): jaki typ klienta/rowerzysty najlepiej trafi w jej ofertę.
4. Krótkie, zachęcające zdanie podsumowujące (1 zdanie).

Całość: 80-150 słów, ton przystępny i profesjonalny. Jeśli podano istniejący opis manualny, potraktuj go
jedynie jako punkt wyjścia/inspirację i napisz go od nowa zgodnie z powyższą strukturą."""


class ManufacturerDescriptionAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_description(self, manufacturer: ManufacturerAiDescriptionRequestDto) -> str:
        if not self._api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured.",
            )

        client = OpenAI(api_key=self._api_key)

        try:
            response = client.chat.completions.create(
                model=self._model,
                temperature=0.7,
                max_tokens=400,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": self._build_user_prompt(manufacturer)},
                ],
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate description from AI provider.",
            ) from exc

        description = response.choices[0].message.content
        if not description:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an empty description.",
            )

        return description.strip()

    @staticmethod
    def _build_user_prompt(manufacturer: ManufacturerAiDescriptionRequestDto) -> str:
        fields = {
            "Nazwa marki": manufacturer.name,
            "Istniejący opis manualny": manufacturer.description,
        }

        lines = [f"{label}: {value}" for label, value in fields.items() if value not in (None, "")]

        return "Dane producenta:\n" + "\n".join(lines)
