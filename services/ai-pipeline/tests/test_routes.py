from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.dependencies import get_gemini_client, get_supabase_client
from app.main import app


def _clients() -> tuple[Mock, Mock]:
    gemini = Mock()
    gemini.models.embed_content.return_value = SimpleNamespace(
        embeddings=[SimpleNamespace(values=[0.1] * 768)]
    )
    gemini.models.generate_content.return_value = SimpleNamespace(
        text="Prudential's technology scale matches how I turn complex systems into results.",
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
                "question_prompt": "Why Prudential?",
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
        model="text-embedding-004", contents="Why Prudential?"
    )
    supabase.rpc.assert_called_once_with(
        "match_stories",
        {"query_embedding": [0.1] * 768, "match_threshold": 0.3, "match_count": 1},
    )
