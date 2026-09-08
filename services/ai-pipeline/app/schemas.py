from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    company_name: str = Field(min_length=1)
    role_title: str = Field(min_length=1)
    question_prompt: str = Field(min_length=1)
    char_limit: int | None = Field(default=600, gt=0)
    writing_sample: str | None = ""
    user_id: str | None = None


class GenerateResponse(BaseModel):
    answer: str
    matched_story_id: str | None = None
    matched_story_title: str | None = None
    grounding_sources: list[str] = Field(default_factory=list)

