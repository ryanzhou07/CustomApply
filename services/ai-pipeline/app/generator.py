import json
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from google import genai
from google.genai import types

from .classifier import QuestionType
from pydantic import BaseModel

from .schemas import GenerateRequest, GenerateResponse

MODEL = "gemini-3.6-flash"


@dataclass(frozen=True)
class GenerationContext:
    id: str
    request: GenerateRequest
    question_type: QuestionType
    story: dict[str, Any] | None


class _GeneratedAnswer(BaseModel):
    id: str
    answer: str


class _GeneratedBatch(BaseModel):
    answers: list[_GeneratedAnswer]


def _system_instruction(char_limit: int, question_type: QuestionType) -> str:
    type_instructions = {
        QuestionType.WHY_COMPANY: (
            "Explain interest in this specific company and connect it to the target role. "
            "Do not reuse motivations or facts about a different company."
        ),
        QuestionType.WHY_ROLE: (
            "Focus on the work performed in this role and bridge it to concrete candidate "
            "evidence from the supplied story."
        ),
        QuestionType.PROJECT: (
            "Focus on why the project mattered, the candidate's specific technical actions, "
            "the decisions made, and the result. Avoid unrelated company filler."
        ),
        QuestionType.ACHIEVEMENT: (
            "Focus on the accomplishment's measurable impact, the candidate's contribution, "
            "and why it was meaningful. Avoid unrelated company filler."
        ),
        QuestionType.GENERAL: "Answer the question directly using the supplied candidate story.",
    }
    return f"""You ghostwrite authentic job-application answers.
{type_instructions[question_type]}
Never invent company facts, personal facts, achievements, motivations, or experience.
Use candidate facts only when they appear in the supplied story. If no story is provided,
do not imply candidate experience. Match the writing sample's sentence structure, cadence,
and tone without copying its facts. Never use these phrases: "testament to", "fostered",
"delved into", "thrilled to apply", or "dynamic fast-paced environment". Return only
the answer. The answer must be no more than {char_limit} characters."""


def _question_guidance(question_type: QuestionType) -> str:
    return {
        QuestionType.WHY_COMPANY: (
            "Explain interest in this specific company and target role. Do not reuse facts "
            "or motivations about another company."
        ),
        QuestionType.WHY_ROLE: (
            "Focus on the role's work and connect it to supplied candidate evidence."
        ),
        QuestionType.PROJECT: (
            "Focus on why the project mattered, technical actions, decisions, and results."
        ),
        QuestionType.ACHIEVEMENT: (
            "Focus on measurable impact, the candidate's contribution, and significance."
        ),
        QuestionType.GENERAL: "Answer directly using only supplied candidate evidence.",
    }[question_type]


def _prompt(
    request: GenerateRequest,
    story: dict[str, Any] | None,
    question_type: QuestionType,
) -> str:
    story_text = json.dumps(story, ensure_ascii=False) if story else "No matching story."
    return f"""Question type: {question_type.value}
Company: {request.company_name}
Role: {request.role_title}
Application question: {request.question_prompt}
Candidate story: {story_text}
Writing sample: {request.writing_sample or "No writing sample provided."}
Character limit: {request.char_limit or 600}"""


def _config(char_limit: int, question_type: QuestionType) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        system_instruction=_system_instruction(char_limit, question_type),
        temperature=0.3,
    )


def _batch_prompt(contexts: list[GenerationContext]) -> str:
    items = [
        {
            "id": context.id,
            "question_type": context.question_type.value,
            "question": context.request.question_prompt,
            "char_limit": context.request.char_limit or 600,
            "guidance": _question_guidance(context.question_type),
            "candidate_story": context.story,
        }
        for context in contexts
    ]
    first = contexts[0].request
    return f"""Generate one independent application answer for every item below.
Preserve every ID and do not combine questions. Respect each item's character limit.
Never invent company or candidate facts. Candidate facts may only come from that item's
candidate_story. Match the writing sample's cadence without copying its facts.

Company: {first.company_name}
Role: {first.role_title}
Writing sample: {first.writing_sample or "No writing sample provided."}
Items: {json.dumps(items, ensure_ascii=False)}"""


def generate_answers(
    contexts: list[GenerationContext], client: genai.Client
) -> dict[str, GenerateResponse]:
    """Generate one or many answers with exactly one Gemini generation request."""
    if not contexts:
        return {}

    response = client.models.generate_content(
        model=MODEL,
        contents=_batch_prompt(contexts),
        config=types.GenerateContentConfig(
            system_instruction=(
                "You ghostwrite concise, authentic job-application answers. Never use these "
                'phrases: "testament to", "fostered", "delved into", "thrilled to apply", '
                'or "dynamic fast-paced environment". Return only the requested JSON.'
            ),
            temperature=0.3,
            response_mime_type="application/json",
            response_schema=_GeneratedBatch,
        ),
    )
    parsed = response.parsed
    if isinstance(parsed, _GeneratedBatch):
        generated = parsed
    elif parsed is not None:
        generated = _GeneratedBatch.model_validate(parsed)
    else:
        generated = _GeneratedBatch.model_validate_json(response.text or "")

    by_id = {item.id: item.answer for item in generated.answers}
    expected_ids = {context.id for context in contexts}
    if set(by_id) != expected_ids or len(generated.answers) != len(contexts):
        raise ValueError("Gemini did not return exactly one answer for every question")

    sources = extract_grounding_sources(response)
    results: dict[str, GenerateResponse] = {}
    for context in contexts:
        char_limit = context.request.char_limit or 600
        story = context.story
        results[context.id] = GenerateResponse(
            answer=by_id[context.id].strip()[:char_limit],
            matched_story_id=(
                str(story["id"]) if story and story.get("id") is not None else None
            ),
            matched_story_title=story.get("title") if story else None,
            grounding_sources=sources,
        )
    return results


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
    request: GenerateRequest,
    story: dict[str, Any] | None,
    question_type: QuestionType,
    client: genai.Client,
) -> GenerateResponse:
    context = GenerationContext(
        id="question-1",
        request=request,
        question_type=question_type,
        story=story,
    )
    return generate_answers([context], client)[context.id]


def stream_answer(
    request: GenerateRequest,
    story: dict[str, Any] | None,
    question_type: QuestionType,
    client: genai.Client,
) -> Iterator[str]:
    char_limit = request.char_limit or 600
    emitted = 0
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=_prompt(request, story, question_type),
        config=_config(char_limit, question_type),
    ):
        text = getattr(chunk, "text", None) or ""
        if not text or emitted >= char_limit:
            continue
        text = text[: char_limit - emitted]
        emitted += len(text)
        yield f"data: {json.dumps({'text': text})}\n\n"
    yield "event: done\ndata: {}\n\n"
