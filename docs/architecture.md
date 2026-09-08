# Architecture scaffold

CustomApply is organized as a small local-first monorepo:

- `apps/dashboard`: React and TypeScript dashboard
- `apps/extension`: TypeScript browser-extension shell
- `services/backend`: FastAPI dashboard API
- `services/ai`: FastAPI service for grounded generation
- `packages/shared`: future shared TypeScript contracts
- `supabase`: PostgreSQL/Supabase configuration and future migrations

Only service entry points and build tooling exist in this scaffold. Workday,
Greenhouse, profile, story bank, tracker, autofill, response generation, citations,
and credential storage are deliberately not implemented.
