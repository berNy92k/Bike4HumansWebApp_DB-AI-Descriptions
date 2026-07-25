import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from starlette import status

from app.models.checkout import Checkout

load_dotenv()

# Fixed structure every generated summary must follow, so admins scanning many
# checkout sessions get a consistent, predictable shape regardless of size/status.
SYSTEM_PROMPT = """Jesteś asystentem panelu administracyjnego sklepu rowerowego. Na podstawie danych sesji
checkout (etap między koszykiem a sfinalizowanym zamówieniem) napisz DOKŁADNIE jeden krótki akapit
(2-3 zdania, po polsku, bez nagłówków, list, markdownu ani emoji), który pomoże administratorowi szybko
zorientować się w tej sesji bez czytania surowej tabeli.

Uwzględnij: co klient wybrał do zakupu (liczba i rodzaj rowerów), łączną wartość, aktualny status oraz
od ilu dni sesja ma ten status (jeśli podano) - to może wskazywać na porzucony checkout. Odnoś się tylko
do podanych danych - nie zmyślaj informacji, których nie podano. Ton rzeczowy, neutralny."""


class CheckoutSummaryAiService:
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)

    def generate_summary(self, checkout: Checkout) -> str:
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
                    {"role": "user", "content": self._build_user_prompt(checkout)},
                ],
            )
        except OpenAIError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate checkout summary from AI provider.",
            ) from exc

        summary = response.choices[0].message.content
        if not summary:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned an empty summary.",
            )

        return summary.strip()

    @staticmethod
    def _build_user_prompt(checkout: Checkout) -> str:
        days_in_status = (
            datetime.now(timezone.utc) - checkout.updated_at.replace(tzinfo=timezone.utc)
        ).days

        item_lines = [
            f"- {item.quantity}x {item.bike.name if item.bike else f'rower (ID {item.bike_id})'}"
            for item in checkout.items
        ]

        fields = {
            "Status": checkout.status,
            "Dni w tym statusie": days_in_status,
            "Łączna wartość": f"{checkout.total_price} {checkout.currency}",
        }
        lines = [f"{label}: {value}" for label, value in fields.items() if value not in (None, "")]

        return "Dane sesji checkout:\n" + "\n".join(lines) + "\n\nProdukty:\n" + "\n".join(item_lines)
