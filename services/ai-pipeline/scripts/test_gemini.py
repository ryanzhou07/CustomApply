"""Make one minimal Gemini generation request to verify API access."""

import sys
from pathlib import Path

from google.genai.errors import APIError

# Allow this file to be run directly from the ai-pipeline directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.dependencies import get_gemini_client
from app.generator import MODEL


def main() -> None:
    try:
        response = get_gemini_client().models.generate_content(
            model=MODEL,
            contents="What is 2 + 2? Reply with only the number.",
        )
    except APIError as error:
        print(f"Gemini request failed ({error.code}): {error.message}")
        raise SystemExit(1) from error

    print(f"Gemini request succeeded: {(response.text or '').strip()}")


if __name__ == "__main__":
    main()
