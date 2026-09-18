# ApplyFlow AI Pipeline

From this directory, install dependencies and start the service:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/fastapi run app/main.py --port 8000
```

Run tests with `.venv/bin/pytest tests/`.

## Batch generation

`POST /api/v1/generate-batch` accepts one to ten questions and generates all answers
with one Gemini generation request. Each question must have a unique frontend ID:

```json
{
  "company_name": "Prudential",
  "role_title": "Software Engineer",
  "writing_sample": "I prefer direct sentences.",
  "user_id": null,
  "questions": [
    {
      "id": "company",
      "question_prompt": "Why Prudential?",
      "char_limit": 600
    },
    {
      "id": "project",
      "question_prompt": "Tell us about a challenging project.",
      "char_limit": 800
    }
  ]
}
```

The existing `/api/v1/generate-answer` and `/api/v1/generate-stream` endpoints remain
available for generating or regenerating a single answer.
