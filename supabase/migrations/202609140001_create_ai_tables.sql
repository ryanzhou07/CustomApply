-- Required for storing 768-dimensional Gemini embeddings.
create extension if not exists vector with schema extensions;

-- Candidate examples used to answer behavioral application questions.
create table public.candidate_stories (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    title text not null,
    situation text,
    task text,
    action text,
    result text,
    embedding extensions.vector(768),
    created_at timestamptz not null default now()
);

-- Original resumes uploaded or entered by a candidate. The database stores
-- metadata and extracted text; the original binary lives in the private
-- Supabase Storage bucket created below.
create table public.resumes (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    name text not null,
    storage_bucket text not null default 'resumes',
    storage_path text,
    original_file_name text,
    mime_type text,
    file_size_bytes bigint,
    raw_text text,
    is_primary boolean not null default false,
    processing_status text not null default 'pending',
    version integer not null default 1,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    deleted_at timestamptz,

    constraint resumes_file_size_valid
        check (file_size_bytes is null or file_size_bytes >= 0),
    constraint resumes_version_valid
        check (version > 0),
    constraint resumes_storage_path_belongs_to_user
        check (
            storage_path is null
            or split_part(storage_path, '/', 1) = user_id::text
        ),
    constraint resumes_id_user_id_unique unique (id, user_id)
);

-- Searchable sections extracted from each resume.
create table public.resume_chunks (
    id uuid primary key default gen_random_uuid(),
    resume_id uuid not null,
    user_id uuid not null references auth.users(id) on delete cascade,
    section_type text,
    title text,
    content text not null,
    embedding extensions.vector(768),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint resume_chunks_resume_owner_fkey
        foreign key (resume_id, user_id)
        references public.resumes(id, user_id)
        on delete cascade
);

-- Private resume files. Objects use the path:
-- {authenticated-user-id}/{resume-id}/{original-filename}
insert into storage.buckets (
    id,
    name,
    public,
    file_size_limit,
    allowed_mime_types
)
values (
    'resumes',
    'resumes',
    false,
    10485760,
    array[
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
)
on conflict (id) do update
set
    public = excluded.public,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

create policy "resume_files_select_own"
    on storage.objects
    for select
    to authenticated
    using (
        bucket_id = 'resumes'
        and (storage.foldername(name))[1] = (select auth.uid()::text)
    );

create policy "resume_files_insert_own"
    on storage.objects
    for insert
    to authenticated
    with check (
        bucket_id = 'resumes'
        and (storage.foldername(name))[1] = (select auth.uid()::text)
    );

create policy "resume_files_update_own"
    on storage.objects
    for update
    to authenticated
    using (
        bucket_id = 'resumes'
        and owner_id = (select auth.uid()::text)
    )
    with check (
        bucket_id = 'resumes'
        and (storage.foldername(name))[1] = (select auth.uid()::text)
    );

create policy "resume_files_delete_own"
    on storage.objects
    for delete
    to authenticated
    using (
        bucket_id = 'resumes'
        and owner_id = (select auth.uid()::text)
    );
