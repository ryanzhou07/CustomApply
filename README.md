# CustomApply

CustomApply is a local-first browser companion for faster, more authentic job applications.

## Why I Am Building This
- Current simplify-style tooling often keeps stronger features in premium plans.
- I want to improve on those limitations by remaking a practical local version.
- The goal is useful automation without forcing users into account-first or premium-only workflows.

## MVP (V1)
- ATS support: Workday and Greenhouse
- Local Profile for core applicant data
- Local Story Bank for response content
- Local Tracker for application progress

## Architecture Scaffold

- `apps/dashboard`: React + TypeScript dashboard
- `apps/extension`: TypeScript browser-extension shell
- `services/backend`: Python + FastAPI dashboard API
- `services/ai`: Python + FastAPI AI service
- `supabase`: Supabase configuration and future PostgreSQL migrations
- `packages/shared`: shared TypeScript contracts

No MVP features are implemented yet.

## Local Setup

Node dependencies are managed from the repository root:

```bash
npm install
npm run typecheck
```

Each Python service uses its own virtual environment:

```bash
python3 -m venv services/backend/.venv
services/backend/.venv/bin/pip install -e 'services/backend[dev]'
python3 -m venv services/ai/.venv
services/ai/.venv/bin/pip install -e 'services/ai[dev]'
npm run dev:backend
npm run dev:ai
```

Run the TypeScript UI projects independently with `npm run dev:dashboard` or
`npm run dev:extension`. Start local Supabase with `npm run supabase:start`.
