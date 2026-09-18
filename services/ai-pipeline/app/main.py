from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google import genai
from supabase import Client

from .classifier import classify_question, should_retrieve_story
from .config import get_settings
from .dependencies import get_gemini_client, get_supabase_client
from .generator import GenerationContext, generate_answer, generate_answers, stream_answer
from .retrieval import retrieve_relevant_story
from .schemas import (
    BatchAnswer,
    GenerateBatchRequest,
    GenerateBatchResponse,
    GenerateRequest,
    GenerateResponse,
)


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
        question_type = classify_question(request.question_prompt)
        story = (
            retrieve_relevant_story(
                request.question_prompt, gemini, supabase, request.user_id
            )
            if should_retrieve_story(question_type)
            else None
        )
        return generate_answer(request, story, question_type, gemini)

    @app.post("/api/v1/generate-stream")
    def answer_stream(
        request: GenerateRequest,
        gemini: genai.Client = Depends(get_gemini_client),
        supabase: Client = Depends(get_supabase_client),
    ) -> StreamingResponse:
        question_type = classify_question(request.question_prompt)
        story = (
            retrieve_relevant_story(
                request.question_prompt, gemini, supabase, request.user_id
            )
            if should_retrieve_story(question_type)
            else None
        )
        return StreamingResponse(
            stream_answer(request, story, question_type, gemini),
            media_type="text/event-stream",
        )

    @app.post("/api/v1/generate-batch", response_model=GenerateBatchResponse)
    def answer_batch(
        request: GenerateBatchRequest,
        gemini: genai.Client = Depends(get_gemini_client),
        supabase: Client = Depends(get_supabase_client),
    ) -> GenerateBatchResponse:
        contexts: list[GenerationContext] = []
        for question in request.questions:
            single_request = GenerateRequest(
                company_name=request.company_name,
                role_title=request.role_title,
                question_prompt=question.question_prompt,
                char_limit=question.char_limit,
                writing_sample=request.writing_sample,
                user_id=request.user_id,
            )
            question_type = classify_question(question.question_prompt)
            story = (
                retrieve_relevant_story(
                    question.question_prompt, gemini, supabase, request.user_id
                )
                if should_retrieve_story(question_type)
                else None
            )
            contexts.append(
                GenerationContext(
                    id=question.id,
                    request=single_request,
                    question_type=question_type,
                    story=story,
                )
            )

        generated = generate_answers(contexts, gemini)
        return GenerateBatchResponse(
            answers=[
                BatchAnswer(
                    id=context.id,
                    question_prompt=context.request.question_prompt,
                    question_type=context.question_type.value,
                    **generated[context.id].model_dump(),
                )
                for context in contexts
            ]
        )

    return app


app = create_app()
