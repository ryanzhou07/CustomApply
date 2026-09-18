create or replace function public.match_resume_chunks(
    query_embedding extensions.vector(768),
    match_threshold float,
    match_count int,
    filter_user_id uuid
)
returns table (
    id uuid,
    resume_id uuid,
    section_type text,
    title text,
    content text,
    similarity float
)
language sql
stable
as $$
    select
        chunk.id,
        chunk.resume_id,
        chunk.section_type,
        chunk.title,
        chunk.content,
        1 - (chunk.embedding <=> query_embedding) as similarity
    from public.resume_chunks as chunk
    where chunk.user_id = filter_user_id
      and chunk.embedding is not null
      and 1 - (chunk.embedding <=> query_embedding) >= match_threshold
    order by chunk.embedding <=> query_embedding
    limit match_count;
$$;
