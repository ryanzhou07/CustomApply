# ApplyFlow AI Pipeline

From this directory, install dependencies and start the service:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/fastapi run app/main.py --port 8000
```

Run tests with `.venv/bin/pytest tests/`.
