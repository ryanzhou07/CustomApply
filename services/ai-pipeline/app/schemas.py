from pydantic import BaseModel, Field, model_validator


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


class BatchQuestion(BaseModel):
    id: str = Field(min_length=1)
    question_prompt: str = Field(min_length=1)
    char_limit: int | None = Field(default=600, gt=0)


class GenerateBatchRequest(BaseModel):
    company_name: str = Field(min_length=1)
    role_title: str = Field(min_length=1)
    questions: list[BatchQuestion] = Field(min_length=1, max_length=10)
    writing_sample: str | None = ""
    user_id: str | None = None

    @model_validator(mode="after")
    def question_ids_must_be_unique(self) -> "GenerateBatchRequest":
        ids = [question.id for question in self.questions]
        if len(ids) != len(set(ids)):
            raise ValueError("Question IDs must be unique")
        return self


class BatchAnswer(GenerateResponse):
    id: str
    question_prompt: str
    question_type: str


class GenerateBatchResponse(BaseModel):
    answers: list[BatchAnswer]
