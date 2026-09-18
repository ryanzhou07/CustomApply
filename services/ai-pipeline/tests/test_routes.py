from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient
from google.genai import types

from app.dependencies import get_gemini_client, get_supabase_client
from app.main import app


def _clients() -> tuple[Mock, Mock]:
    gemini = Mock()
    gemini.models.embed_content.return_value = SimpleNamespace(
        embeddings=[SimpleNamespace(values=[0.1] * 768)]
    )
    gemini.models.generate_content.return_value = SimpleNamespace(
        text="",
        parsed={
            "answers": [
                {
                    "id": "question-1",
                    "answer": (
                        "Prudential's technology scale matches how I turn complex systems "
                        "into results."
                    ),
                }
            ]
        },
        candidates=[
            SimpleNamespace(
                grounding_metadata=SimpleNamespace(
                    grounding_chunks=[
                        SimpleNamespace(web=SimpleNamespace(uri="https://example.com/source"))
                    ]
                )
            )
        ],
    )

    supabase = Mock()
    supabase.rpc.return_value.execute.return_value = SimpleNamespace(
        data=[
            {
                "id": "story-1",
                "title": "Scaling a platform",
                "situation": "A service was overloaded.",
                "task": "Improve reliability.",
                "action": "I redesigned its queueing layer.",
                "result": "Latency fell by 40%.",
            }
        ]
    )
    return gemini, supabase


def test_health() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_generate_answer_rejects_missing_fields() -> None:
    gemini, supabase = _clients()
    app.dependency_overrides[get_gemini_client] = lambda: gemini
    app.dependency_overrides[get_supabase_client] = lambda: supabase
    try:
        response = TestClient(app).post(
            "/api/v1/generate-answer", json={"company_name": "Prudential"}
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 422


def test_generate_answer_with_mocked_services() -> None:
    gemini, supabase = _clients()
    app.dependency_overrides[get_gemini_client] = lambda: gemini
    app.dependency_overrides[get_supabase_client] = lambda: supabase
    try:
        response = TestClient(app).post(
            "/api/v1/generate-answer",
            json={
                "company_name": "Prudential",
                "role_title": "Software Engineer",
                "question_prompt": "Tell us about a challenging project.",
                "char_limit": 600,
                "writing_sample": "I prefer direct sentences.",
                "user_id": "user-1",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Prudential's technology scale matches how I turn complex systems into results.",
        "matched_story_id": "story-1",
        "matched_story_title": "Scaling a platform",
        "grounding_sources": ["https://example.com/source"],
    }
    gemini.models.embed_content.assert_called_once_with(
        model="gemini-embedding-2",
        contents="Tell us about a challenging project.",
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    supabase.rpc.assert_called_once_with(
        "match_stories",
        {
            "query_embedding": [0.1] * 768,
            "match_threshold": 0.3,
            "match_count": 1,
            "filter_user_id": "user-1",
        },
    )


def test_generate_batch_uses_one_generation_call_for_multiple_questions() -> None:
    gemini, supabase = _clients()
    gemini.models.generate_content.return_value.parsed = {
        "answers": [
            {"id": "company", "answer": "I value Prudential's long-term impact."},
            {"id": "project", "answer": "I redesigned a queue to reduce latency."},
        ]
    }
    app.dependency_overrides[get_gemini_client] = lambda: gemini
    app.dependency_overrides[get_supabase_client] = lambda: supabase
    try:
        response = TestClient(app).post(
            "/api/v1/generate-batch",
            json={
                "company_name": "Prudential",
                "role_title": "Software Engineer",
                "writing_sample": "I prefer direct sentences.",
                "user_id": "user-1",
                "questions": [
                    {
                        "id": "company",
                        "question_prompt": "Why Prudential?",
                        "char_limit": 600,
                    },
                    {
                        "id": "project",
                        "question_prompt": "Tell us about a challenging project.",
                        "char_limit": 600,
                    },
                ],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    answers = response.json()["answers"]
    assert [answer["id"] for answer in answers] == ["company", "project"]
    assert answers[0]["question_type"] == "why_company"
    assert answers[0]["matched_story_id"] is None
    assert answers[1]["question_type"] == "project"
    assert answers[1]["matched_story_id"] == "story-1"
    assert gemini.models.generate_content.call_count == 1
    assert gemini.models.embed_content.call_count == 1
    assert supabase.rpc.call_count == 1


def test_generate_batch_handles_one_question() -> None:
    gemini, supabase = _clients()
    gemini.models.generate_content.return_value.parsed = {
        "answers": [{"id": "company", "answer": "A concise company answer."}]
    }
    app.dependency_overrides[get_gemini_client] = lambda: gemini
    app.dependency_overrides[get_supabase_client] = lambda: supabase
    try:
        response = TestClient(app).post(
            "/api/v1/generate-batch",
            json={
                "company_name": "Prudential",
                "role_title": "Software Engineer",
                "questions": [
                    {"id": "company", "question_prompt": "Why Prudential?"}
                ],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()["answers"]) == 1
    assert response.json()["answers"][0]["answer"] == "A concise company answer."
    assert gemini.models.generate_content.call_count == 1
    gemini.models.embed_content.assert_not_called()
    supabase.rpc.assert_not_called()


def test_generate_batch_rejects_empty_questions() -> None:
    gemini, supabase = _clients()
    app.dependency_overrides[get_gemini_client] = lambda: gemini
    app.dependency_overrides[get_supabase_client] = lambda: supabase
    try:
        response = TestClient(app).post(
            "/api/v1/generate-batch",
            json={
                "company_name": "Prudential",
                "role_title": "Software Engineer",
                "questions": [],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
