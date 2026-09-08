from datetime import UTC, date, datetime
from enum import StrEnum

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="CustomApply Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobStatus(StrEnum):
    wishlist = "Wishlist"
    applied = "Applied"
    interview = "Interview"
    offer = "Offer"
    rejected = "Rejected"


class JobInput(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=160)
    location: str = Field(default="Remote", max_length=160)
    status: JobStatus = JobStatus.wishlist


class Job(JobInput):
    id: int
    applied: date | None = None


class SavedResponseInput(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)
    answer: str = Field(min_length=1, max_length=10_000)
    category: str = Field(default="General", max_length=80)


class SavedResponse(SavedResponseInput):
    id: int


jobs: dict[int, Job] = {}
responses: dict[int, SavedResponse] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/jobs", response_model=list[Job])
def list_jobs() -> list[Job]:
    return list(jobs.values())


@app.post("/api/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobInput) -> Job:
    job_id = max(jobs, default=0) + 1
    item = Job(id=job_id, **payload.model_dump())
    if payload.status != JobStatus.wishlist:
        item.applied = datetime.now(UTC).date()
    jobs[job_id] = item
    return item


@app.patch("/api/jobs/{job_id}", response_model=Job)
def update_job(job_id: int, payload: JobInput) -> Job:
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    item = Job(id=job_id, **payload.model_dump())
    item.applied = jobs[job_id].applied
    jobs[job_id] = item
    return item


@app.delete("/api/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int) -> Response:
    if jobs.pop(job_id, None) is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api/responses", response_model=list[SavedResponse])
def list_responses() -> list[SavedResponse]:
    return list(responses.values())


@app.post("/api/responses", response_model=SavedResponse, status_code=status.HTTP_201_CREATED)
def create_response(payload: SavedResponseInput) -> SavedResponse:
    response_id = max(responses, default=0) + 1
    item = SavedResponse(id=response_id, **payload.model_dump())
    responses[response_id] = item
    return item
