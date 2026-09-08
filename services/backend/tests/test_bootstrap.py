from fastapi.testclient import TestClient

from app.main import app


def test_application_metadata() -> None:
    assert app.title == "CustomApply Backend"


def test_health_and_job_lifecycle() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    created = client.post(
        "/api/jobs",
        json={"company": "Acme", "role": "Engineer", "location": "Remote"},
    )
    assert created.status_code == 201
    job_id = created.json()["id"]
    assert client.get("/api/jobs").json()[-1]["company"] == "Acme"
    assert client.delete(f"/api/jobs/{job_id}").status_code == 204


def test_response_validation() -> None:
    client = TestClient(app)
    assert client.post("/api/responses", json={"prompt": "", "answer": ""}).status_code == 422
