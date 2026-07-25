import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.models.cart import Cart

load_dotenv()

# Fixed structure every generated summary must follow, so admins scanning many
# carts get a consistent, predictable shape regardless of size/status.
SYSTEM_PROMPT = """Jesteś asystentem panelu administracyjnego sklepu rowerowego. Na podstawie danych koszyka
klienta napisz DOKŁADNIE jeden krótki akapit (2-3 zdania, po polsku, bez nagłówków, list, markdownu ani emoji),
który pomoże administratorowi szybko zorientować się w tym koszyku bez czytania surowej tabeli.

Uwzględnij: co znajduje się w koszyku (liczba i rodzaj rowerów), przybliżoną łączną wartość, aktualny status
oraz od ilu dni koszyk nie był aktualizowany (jeśli podano) - długi czas bez aktywności przy statusie
oczekującym może oznaczać porzucony koszyk, o czym możesz wspomnieć. Odnoś się tylko do podanych danych -
nie zmyślaj informacji, których nie podano. Ton rzeczowy, neutralny."""


class CartSummaryAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_summary(self, cart: Cart) -> str:
        if not self._api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured.",
            )

        client = OpenAI(api_key=self._api_key)

        try:
            response = client.chat.completions.create(
                model=self._model,
                temperature=0.4,
                max_tokens=200,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": self._build_user_prompt(cart)},
                ],
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate cart summary from AI provider.",
            ) from exc

        summary = response.choices[0].message.content
        if not summary:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an empty summary.",
            )

        return summary.strip()

    @staticmethod
    def _build_user_prompt(cart: Cart) -> str:
        days_since_update = (
            datetime.now(timezone.utc) - cart.updated_at.replace(tzinfo=timezone.utc)
        ).days

        total_price = sum(
            (item.bike.price if item.bike else 0) * item.quantity for item in cart.items
        )

        item_lines = [
            f"- {item.quantity}x {item.bike.name if item.bike else f'rower (ID {item.bike_id})'}"
            for item in cart.items
        ]

        fields = {
            "Status": cart.status,
            "Dni bez aktualizacji": days_since_update,
            "Przybliżona łączna wartość": f"{total_price} {cart.currency}",
        }
        lines = [f"{label}: {value}" for label, value in fields.items() if value not in (None, "")]

        return "Dane koszyka:\n" + "\n".join(lines) + "\n\nProdukty:\n" + "\n".join(item_lines)
