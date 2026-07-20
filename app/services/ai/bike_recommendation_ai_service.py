import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.models.bike import Bike

load_dotenv()

SYSTEM_PROMPT = """Jesteś doradcą sklepu rowerowego. Klient ogląda konkretny rower, a Ty dostajesz listę
kilku podobnych propozycji z tego samego sklepu.

Napisz DOKŁADNIE jeden krótki akapit (2-3 zdania, po polsku, bez nagłówków, list, markdownu ani emoji),
który ogólnie wyjaśnia, dlaczego te propozycje mogą zainteresować klienta oglądającego dany rower -
odnoś się tylko do podanych danych (typ roweru, przeznaczenie, cena, grupa docelowa) i nie zmyślaj cech,
których nie podano. Nie wymieniaj pojedynczo nazw modeli - pisz ogólnie o tej grupie propozycji.

Całość: maksymalnie 60 słów, ton przyjazny i pomocny."""


class BikeRecommendationAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_recommendation_note(self, bike: Bike, similar_bikes: list[Bike]) -> str:
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
                max_tokens=200,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": self._build_user_prompt(bike, similar_bikes)},
                ],
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate recommendation note from AI provider.",
            ) from exc

        note = response.choices[0].message.content
        if not note:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an empty recommendation note.",
            )

        return note.strip()

    @staticmethod
    def _build_user_prompt(bike: Bike, similar_bikes: list[Bike]) -> str:
        current = {
            "Nazwa": bike.name,
            "Typ roweru": bike.bike_type,
            "Przeznaczenie": bike.usage,
            "Dla kogo": bike.target_user,
            "Cena": bike.price,
        }
        current_lines = [f"{label}: {value}" for label, value in current.items() if value not in (None, "")]

        similar_lines = []
        for similar in similar_bikes:
            fields = {
                "typ": similar.bike_type,
                "przeznaczenie": similar.usage,
                "cena": similar.price,
            }
            details = ", ".join(f"{k}: {v}" for k, v in fields.items() if v not in (None, ""))
            similar_lines.append(f"- {details}")

        return (
            "Oglądany rower:\n"
            + "\n".join(current_lines)
            + "\n\nPropozycje podobnych rowerów:\n"
            + "\n".join(similar_lines)
        )
