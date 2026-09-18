# Supabase database

This directory is the single database boundary shared by the backend and AI pipeline.
Do not duplicate these migrations inside either service.

## Starter migration

The initial migration is:

```text
migrations/202609140001_create_ai_tables.sql
```

Supabase requires the numeric timestamp prefix to track migration order. The readable
name after the underscore explains its purpose. This starter migration enables
pgvector, creates `candidate_stories`, `resumes`, and `resume_chunks`, and provisions
the private `resumes` Storage bucket next to the resume schema.

The next migration adds the story retrieval function used by the AI pipeline:

```text
migrations/202609140002_match_stories.sql
```

The third migration adds semantic retrieval for relevant resume sections:

```text
migrations/202609140003_match_resume_chunks.sql
```

The platform migration adds the user-facing application data model:

```text
migrations/202609170001_create_platform_schema.sql
```

It creates Google-backed `user_profiles`, job `applications`, reusable saved
responses, per-application response records, indexes, and Row Level Security. It
also adds ownership policies to the earlier resume and AI tables.

Resume objects must be uploaded through the Supabase Storage API using this path:

```text
{authenticated-user-id}/{resume-id}/{original-filename}
```

The database stores the object path and file metadata; the binary file stays in
the private `resumes` Storage bucket.

## Apply locally first

Start Docker Desktop, then run these commands from the repository root:

```bash
npm run supabase:start
npx supabase migration list --local
npx supabase db reset
```

`db reset` deletes and recreates only the local Supabase database, applies every
migration in order, and then runs `seed.sql`. Do not run it against a database that
contains local data you need to retain.

After the reset succeeds, inspect the tables and policies in local Studio at
<http://127.0.0.1:54323> and run:

```bash
npx supabase db lint --local --level warning
```

## Apply to a hosted project

Only after local verification, link the CLI to the intended Supabase project and
review the pending migration list before pushing:

```bash
npx supabase link --project-ref YOUR_PROJECT_REF
npx supabase migration list
npx supabase db push --dry-run
npx supabase db push
```

Linking and pushing affect external state. Confirm the project reference carefully,
and never commit database passwords, secret keys, or `.env` files.

The Supabase secret key remains server-side and must never use a `VITE_` prefix.
