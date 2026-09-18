-- CustomApply platform tables
--
-- Supabase Auth owns authentication data in auth.users. The tables below hold
-- product data that belongs to each authenticated user.

-- -----------------------------------------------------------------------------
-- Shared updated_at helper
-- -----------------------------------------------------------------------------

create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

-- -----------------------------------------------------------------------------
-- User profiles
-- -----------------------------------------------------------------------------

create table public.user_profiles (
    id uuid primary key references auth.users(id) on delete cascade,

    -- Values supplied by Google through Supabase Auth.
    email text,
    full_name text,
    given_name text,
    family_name text,
    avatar_url text,
    locale text,
    auth_provider text not null default 'google',
    provider_user_id text,
    email_verified boolean not null default false,
    provider_metadata jsonb not null default '{}'::jsonb,

    -- Values managed by CustomApply.
    preferred_name text,
    phone text,
    location text,
    linkedin_url text,
    preferences jsonb not null default '{}'::jsonb,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- Copy the Google profile fields into public.user_profiles whenever Supabase
-- creates or updates an authenticated user.
create or replace function public.sync_auth_user_profile()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
    insert into public.user_profiles (
        id,
        email,
        full_name,
        given_name,
        family_name,
        avatar_url,
        locale,
        auth_provider,
        provider_user_id,
        email_verified,
        provider_metadata,
        created_at,
        updated_at
    )
    values (
        new.id,
        new.email,
        coalesce(
            new.raw_user_meta_data ->> 'full_name',
            new.raw_user_meta_data ->> 'name'
        ),
        new.raw_user_meta_data ->> 'given_name',
        new.raw_user_meta_data ->> 'family_name',
        coalesce(
            new.raw_user_meta_data ->> 'avatar_url',
            new.raw_user_meta_data ->> 'picture'
        ),
        new.raw_user_meta_data ->> 'locale',
        coalesce(new.raw_app_meta_data ->> 'provider', 'email'),
        coalesce(
            new.raw_user_meta_data ->> 'provider_id',
            new.raw_user_meta_data ->> 'sub'
        ),
        new.email_confirmed_at is not null,
        coalesce(new.raw_user_meta_data, '{}'::jsonb),
        coalesce(new.created_at, now()),
        now()
    )
    on conflict (id) do update
    set
        email = excluded.email,
        full_name = excluded.full_name,
        given_name = excluded.given_name,
        family_name = excluded.family_name,
        avatar_url = excluded.avatar_url,
        locale = excluded.locale,
        auth_provider = excluded.auth_provider,
        provider_user_id = excluded.provider_user_id,
        email_verified = excluded.email_verified,
        provider_metadata = excluded.provider_metadata,
        updated_at = now();

    return new;
end;
$$;

create trigger sync_auth_user_profile_after_change
    after insert or update of
        email,
        email_confirmed_at,
        raw_user_meta_data,
        raw_app_meta_data
    on auth.users
    for each row
    execute function public.sync_auth_user_profile();

-- Backfill anyone who signed in before this migration was applied.
insert into public.user_profiles (
    id,
    email,
    full_name,
    given_name,
    family_name,
    avatar_url,
    locale,
    auth_provider,
    provider_user_id,
    email_verified,
    provider_metadata,
    created_at,
    updated_at
)
select
    auth_user.id,
    auth_user.email,
    coalesce(
        auth_user.raw_user_meta_data ->> 'full_name',
        auth_user.raw_user_meta_data ->> 'name'
    ),
    auth_user.raw_user_meta_data ->> 'given_name',
    auth_user.raw_user_meta_data ->> 'family_name',
    coalesce(
        auth_user.raw_user_meta_data ->> 'avatar_url',
        auth_user.raw_user_meta_data ->> 'picture'
    ),
    auth_user.raw_user_meta_data ->> 'locale',
    coalesce(auth_user.raw_app_meta_data ->> 'provider', 'email'),
    coalesce(
        auth_user.raw_user_meta_data ->> 'provider_id',
        auth_user.raw_user_meta_data ->> 'sub'
    ),
    auth_user.email_confirmed_at is not null,
    coalesce(auth_user.raw_user_meta_data, '{}'::jsonb),
    auth_user.created_at,
    now()
from auth.users as auth_user
on conflict (id) do nothing;

create trigger set_user_profiles_updated_at
    before update on public.user_profiles
    for each row
    execute function public.set_updated_at();

-- -----------------------------------------------------------------------------
-- Job applications
-- -----------------------------------------------------------------------------

create table public.applications (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.user_profiles(id) on delete cascade,
    company_name text not null,
    role_title text not null,
    status text not null default 'wishlist',
    job_url text,
    location text,
    description text,
    notes text,
    applied_at timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    -- This pair lets child records prove that they belong to both the
    -- application and the same user.
    unique (id, user_id)
);

create index applications_user_id_updated_at_idx
    on public.applications (user_id, updated_at desc);

create index applications_user_id_status_idx
    on public.applications (user_id, status);

create trigger set_applications_updated_at
    before update on public.applications
    for each row
    execute function public.set_updated_at();

-- -----------------------------------------------------------------------------
-- Resumes
-- -----------------------------------------------------------------------------

-- The resume table, extracted chunks, private Storage bucket, and file policies
-- are created together in 202609140001_create_ai_tables.sql.

create index resumes_user_id_updated_at_idx
    on public.resumes (user_id, updated_at desc)
    where deleted_at is null;

create unique index resumes_one_primary_per_user_idx
    on public.resumes (user_id)
    where is_primary and deleted_at is null;

create index resume_chunks_user_id_idx
    on public.resume_chunks (user_id);

create index resume_chunks_resume_id_idx
    on public.resume_chunks (resume_id);

create trigger set_resumes_updated_at
    before update on public.resumes
    for each row
    execute function public.set_updated_at();

create trigger set_resume_chunks_updated_at
    before update on public.resume_chunks
    for each row
    execute function public.set_updated_at();

-- -----------------------------------------------------------------------------
-- Reusable responses and writing samples
-- -----------------------------------------------------------------------------

create table public.saved_responses (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.user_profiles(id) on delete cascade,
    category text,
    prompt text not null,
    answer text not null,
    response_type text not null default 'question_answer',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index saved_responses_user_id_updated_at_idx
    on public.saved_responses (user_id, updated_at desc);

create trigger set_saved_responses_updated_at
    before update on public.saved_responses
    for each row
    execute function public.set_updated_at();

-- -----------------------------------------------------------------------------
-- Responses written for a specific application
-- -----------------------------------------------------------------------------

create table public.application_responses (
    id uuid primary key default gen_random_uuid(),
    application_id uuid not null,
    user_id uuid not null references public.user_profiles(id) on delete cascade,
    question_text text not null,
    answer_text text,
    status text not null default 'draft',
    character_limit integer,
    is_ai_generated boolean not null default false,
    ai_model text,
    submitted_at timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    foreign key (application_id, user_id)
        references public.applications(id, user_id)
        on delete cascade
);

create index application_responses_application_id_idx
    on public.application_responses (application_id);

create index application_responses_user_id_updated_at_idx
    on public.application_responses (user_id, updated_at desc);

create trigger set_application_responses_updated_at
    before update on public.application_responses
    for each row
    execute function public.set_updated_at();

-- -----------------------------------------------------------------------------
-- Row Level Security
-- -----------------------------------------------------------------------------

-- Frontend route guards improve the user experience, but they are not a
-- security boundary. RLS protects the database even when someone calls the
-- Supabase API directly with the public key.

alter table public.user_profiles enable row level security;
alter table public.applications enable row level security;
alter table public.resumes enable row level security;
alter table public.resume_chunks enable row level security;
alter table public.saved_responses enable row level security;
alter table public.application_responses enable row level security;
alter table public.candidate_stories enable row level security;

create policy "users_read_own_profile"
    on public.user_profiles
    for select
    to authenticated
    using ((select auth.uid()) = id);

create policy "users_update_own_profile"
    on public.user_profiles
    for update
    to authenticated
    using ((select auth.uid()) = id)
    with check ((select auth.uid()) = id);

create policy "users_manage_own_applications"
    on public.applications
    for all
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

create policy "users_manage_own_resumes"
    on public.resumes
    for all
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

create policy "users_manage_own_resume_chunks"
    on public.resume_chunks
    for all
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

create policy "users_manage_own_saved_responses"
    on public.saved_responses
    for all
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

create policy "users_manage_own_application_responses"
    on public.application_responses
    for all
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

create policy "users_manage_own_candidate_stories"
    on public.candidate_stories
    for all
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

-- These grants expose CRUD operations through Supabase's generated Data API.
-- The RLS policies above still decide which rows each user can access.
grant select on table public.user_profiles to authenticated;

-- Supabase projects may grant table-level updates by default. Remove that broad
-- permission, then allow edits only to fields owned by CustomApply.
revoke update on table public.user_profiles from authenticated;
grant update (
    preferred_name,
    phone,
    location,
    linkedin_url,
    preferences
) on table public.user_profiles to authenticated;

grant select, insert, update, delete on table public.applications to authenticated;
grant select, insert, update, delete on table public.resumes to authenticated;
grant select, insert, update, delete on table public.resume_chunks to authenticated;
grant select, insert, update, delete on table public.saved_responses to authenticated;
grant select, insert, update, delete on table public.application_responses to authenticated;
grant select, insert, update, delete on table public.candidate_stories to authenticated;
