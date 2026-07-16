import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.schemas.admin.bike.admin_bike_ai_description_request_dto import BikeAiDescriptionRequestDto

load_dotenv()

SYSTEM_PROMPT = """Jesteś copywriterem sklepu rowerowego. Piszesz opisy produktowe rowerów po polsku.

Każdy opis MUSI się składać z dokładnie 4 akapitów, w tej kolejności, oddzielonych pojedynczą pustą linią,
bez nagłówków, list, markdownu ani emoji:
1. Chwytliwe wprowadzenie (1-2 zdania) przedstawiające model roweru i jego ogólny charakter.
2. Cechy techniczne (2-4 zdania) opisujące naturalnym językiem tylko te parametry, które zostały podane
   w danych wejściowych (np. rama, koła, napęd, hamulce, zawieszenie, waga) - nie zmyślaj brakujących danych.
3. Dla kogo jest ten rower (1-2 zdania): poziom zaawansowania, zastosowanie, zalecany wzrost - jeśli podano.
4. Krótkie, zachęcające zdanie podsumowujące (1 zdanie).

Całość: 80-150 słów, ton przystępny i profesjonalny. Jeśli podano istniejący opis manualny, potraktuj go
jedynie jako punkt wyjścia/inspirację i napisz go od nowa zgodnie z powyższą strukturą."""


class BikeDescriptionAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_description(self, bike: BikeAiDescriptionRequestDto) -> str:
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
                    {"role": "user", "content": self._build_user_prompt(bike)},
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
    def _build_user_prompt(bike: BikeAiDescriptionRequestDto) -> str:
        fields = {
            "Nazwa": bike.name,
            "Istniejący opis manualny": bike.description,
            "Typ roweru": bike.bike_type,
            "Materiał ramy": bike.frame_material,
            "Rozmiar ramy": bike.frame_size,
            "Rozmiar ramy (etykieta)": bike.frame_size_label,
            "Rozmiar kół (cale)": bike.wheel_size,
            "Szerokość opon (mm)": bike.tire_width,
            "Liczba biegów": bike.gear_count,
            "Hamulce": bike.brake_type,
            "Zawieszenie": bike.suspension_type,
            "Kolor": bike.color,
            "Waga (kg)": bike.weight_kg,
            "Zalecany wzrost min (cm)": bike.recommended_height_min,
            "Zalecany wzrost max (cm)": bike.recommended_height_max,
            "Zastosowanie": bike.usage,
            "Dla kogo": bike.target_user,
        }

        lines = [f"{label}: {value}" for label, value in fields.items() if value not in (None, "")]

        return "Dane roweru:\n" + "\n".join(lines)
