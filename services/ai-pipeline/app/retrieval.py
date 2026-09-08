from typing import Any

from google import genai
from supabase import Client


def _embedding_values(response: Any) -> list[float]:
    """Support the typed SDK response and simple test doubles."""
    embeddings = getattr(response, "embeddings", None)
    if embeddings:
        values = getattr(embeddings[0], "values", None)
        if values is not None:
            return list(values)
    embedding = getattr(response, "embedding", None)
    values = getattr(embedding, "values", embedding)
    if values is not None:
        return list(values)
    raise ValueError("Gemini returned no embedding values")


def retrieve_relevant_story(
    question: str, client: genai.Client, supabase: Client
) -> dict[str, Any] | None:
    response = client.models.embed_content(model="text-embedding-004", contents=question)
    query_embedding = _embedding_values(response)
    if len(query_embedding) != 768:
        raise ValueError(f"Expected a 768-dimensional embedding, got {len(query_embedding)}")

    result = supabase.rpc(
        "match_stories",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.3,
            "match_count": 1,
        },
    ).execute()
    rows = result.data or []
    if not rows:
        return None

    story = rows[0]
    return {
        key: story.get(key)
        for key in ("id", "title", "situation", "task", "action", "result")
    }

