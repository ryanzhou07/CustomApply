import json
from collections.abc import Iterator
from typing import Any

from google import genai
from google.genai import types

from .schemas import GenerateRequest, GenerateResponse

MODEL = "gemini-2.5-flash"


def _system_instruction(char_limit: int) -> str:
    return f"""You ghostwrite authentic job-application answers.
Use a strict 50/50 anchor: approximately half the answer must cite concrete, current
company initiatives or technology scale found through Google Search, and half must
bridge those details to the candidate's supplied story. Never invent personal facts,
achievements, motivations, or experience absent from that story. If no story is
provided, do not imply one. Match the writing sample's sentence structure, cadence,
and tone without copying its facts. Never use these phrases: "testament to",
"fostered", "delved into", "thrilled to apply", or "dynamic fast-paced environment".
Return only the answer. The answer must be no more than {char_limit} characters."""


def _prompt(request: GenerateRequest, story: dict[str, Any] | None) -> str:
    story_text = json.dumps(story, ensure_ascii=False) if story else "No matching story."
    return f"""Company: {request.company_name}
            Role: {request.role_title}
            Application question: {request.question_prompt}
            Candidate story: {story_text}
            Writing sample: {request.writing_sample or "No writing sample provided."}
            Character limit: {request.char_limit or 600}"""


def _config(char_limit: int) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        system_instruction=_system_instruction(char_limit),
        temperature=0.3,
        tools=[types.Tool(google_search=types.GoogleSearch())],
    )


def extract_grounding_sources(response: Any) -> list[str]:
    sources: list[str] = []
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        metadata = getattr(candidate, "grounding_metadata", None)
        for chunk in getattr(metadata, "grounding_chunks", None) or []:
            web = getattr(chunk, "web", None)
            uri = getattr(web, "uri", None)
            if uri and uri not in sources:
                sources.append(uri)
    return sources


def generate_answer(
    request: GenerateRequest, story: dict[str, Any] | None, client: genai.Client
) -> GenerateResponse:
    char_limit = request.char_limit or 600
    response = client.models.generate_content(
        model=MODEL,
        contents=_prompt(request, story),
        config=_config(char_limit),
    )
    answer = (response.text or "").strip()[:char_limit]
    return GenerateResponse(
        answer=answer,
        matched_story_id=str(story["id"]) if story and story.get("id") is not None else None,
        matched_story_title=story.get("title") if story else None,
        grounding_sources=extract_grounding_sources(response),
    )


def stream_answer(
    request: GenerateRequest, story: dict[str, Any] | None, client: genai.Client
) -> Iterator[str]:
    char_limit = request.char_limit or 600
    emitted = 0
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=_prompt(request, story),
        config=_config(char_limit),
    ):
        text = getattr(chunk, "text", None) or ""
        if not text or emitted >= char_limit:
            continue
        text = text[: char_limit - emitted]
        emitted += len(text)
        yield f"data: {json.dumps({'text': text})}\n\n"
    yield "event: done\ndata: {}\n\n"

