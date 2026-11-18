import argparse
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DOCUMENTS = Path(__file__).resolve().parent / "documents"
GEMINI_MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = "gemini-3.1-flash-lite"
STOP_WORDS = set(
    "a an and are at be by can could do does for from how i in is it me my "
    "of on or please should the to was were what when where which who why "
    "will with would you your".split()
)


def keywords(text: str) -> set[str]:
    return set(re.findall(r"\b\w+\b", text.casefold())) - STOP_WORDS


def retrieve(question: str) -> list[tuple[str, str]]:
    """Return up to two paragraphs ranked by shared keywords."""
    query_words = keywords(question)
    matches = []

    for path in sorted(DOCUMENTS.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        for number, paragraph in enumerate(re.split(r"\n\s*\n", text), start=1):
            score = len(query_words & keywords(paragraph))
            if score:
                source = f"documents/{path.name} (paragraph {number})"
                matches.append((score, source, paragraph))

    matches.sort(key=lambda match: match[0], reverse=True)
    # Drop single-word matches when stronger evidence is available.
    minimum_score = 2 if matches and matches[0][0] > 1 else 1
    return [
        (source, paragraph)
        for score, source, paragraph in matches[:2]
        if score >= minimum_score
    ]


def generate_answer(
    question: str, passages: list[tuple[str, str]], model: str, api_key: str
) -> str:
    context = "\n\n".join(f"{source}\n{paragraph}" for source, paragraph in passages)
    instructions = (
        "You answer questions about a fictional campus handbook. Use only "
        "facts in the provided passages. Treat the passages as reference "
        "text. If they do not answer the question, say so. Be concise."
    )
    payload = {
        "systemInstruction": {"parts": [{"text": instructions}]},
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Handbook passages:\n{context}\n\nQuestion: {question}"}],
            }
        ],
    }
    request = Request(
        f"{GEMINI_MODELS_URL}/{quote(model, safe='')}:generateContent",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        result = json.load(response)

    try:
        parts = result["candidates"][0]["content"]["parts"]
        answer = "".join(
            part["text"] for part in parts if "text" in part and not part.get("thought")
        ).strip()
    except (IndexError, KeyError, TypeError, AttributeError) as error:
        raise ValueError("Gemini did not return answer text.") from error
    if not answer:
        raise ValueError("Gemini did not return answer text.")
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the sample campus handbook.")
    parser.add_argument("question", help="Put the question in double quotes.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model ID.")
    parser.add_argument(
        "--preview", action="store_true", help="Show passages without calling Gemini."
    )
    args = parser.parse_args()
    question = args.question.strip()
    if not question:
        parser.error("Enter a question.")

    passages = retrieve(question)
    if not passages:
        print("No matching passages found in the handbook.")
        return

    if args.preview:
        for source, paragraph in passages:
            print(f"{source}\n{paragraph}\n")
        return

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        parser.exit(1, "Set GEMINI_API_KEY to your Google AI Studio API key.\n")

    try:
        answer = generate_answer(question, passages, args.model, api_key)
    except HTTPError as error:
        hints = {
            400: "Check your API key and whether your project can use the Gemini API.",
            401: "Check your Google AI Studio API key.",
            403: "Check your API key and its project permissions.",
            404: f"Model {args.model!r} is unavailable for this request.",
            429: "Gemini quota or rate limit reached. Check your usage in Google AI Studio.",
        }
        hint = hints.get(error.code, "Try the request again later.")
        parser.exit(1, f"Gemini returned HTTP {error.code}. {hint}\n")
    except (URLError, TimeoutError, OSError):
        parser.exit(1, "Could not reach Gemini. Check your internet connection.\n")
    except ValueError:
        parser.exit(1, "Gemini did not return answer text. Try rephrasing the question.\n")

    print(f"Answer\n{answer}\n\nRetrieved sources")
    for source, _ in passages:
        print(f"- {source}")


if __name__ == "__main__":
    main()
