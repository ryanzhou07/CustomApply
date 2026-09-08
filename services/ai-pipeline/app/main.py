from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google import genai
from supabase import Client

from .config import get_settings
from .dependencies import get_gemini_client, get_supabase_client
from .generator import generate_answer, stream_answer
from .retrieval import retrieve_relevant_story
from .schemas import GenerateRequest, GenerateResponse


def create_app() -> FastAPI:
    app = FastAPI(title="ApplyFlow AI Pipeline", version="1.0.0")
    try:
        origins = get_settings().cors_origins
    except Exception:
        # Preserve importability for health checks and tests before secrets are configured.
        origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=origins != ["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy"}

    @app.post("/api/v1/generate-answer", response_model=GenerateResponse)
    def answer(
        request: GenerateRequest,
        gemini: genai.Client = Depends(get_gemini_client),
        supabase: Client = Depends(get_supabase_client),
    ) -> GenerateResponse:
        story = retrieve_relevant_story(request.question_prompt, gemini, supabase)
        return generate_answer(request, story, gemini)

    @app.post("/api/v1/generate-stream")
    def answer_stream(
        request: GenerateRequest,
        gemini: genai.Client = Depends(get_gemini_client),
        supabase: Client = Depends(get_supabase_client),
    ) -> StreamingResponse:
        story = retrieve_relevant_story(request.question_prompt, gemini, supabase)
        return StreamingResponse(
            stream_answer(request, story, gemini), media_type="text/event-stream"
        )

    return app


app = create_app()

