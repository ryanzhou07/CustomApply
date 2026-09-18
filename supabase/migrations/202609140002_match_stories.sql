create or replace function public.match_stories(
    query_embedding extensions.vector(768),
    match_threshold float,
    match_count int,
    filter_user_id uuid
)
returns table (
    id uuid,
    title text,
    situation text,
    task text,
    action text,
    result text,
    similarity float
)
language sql
stable
as $$
    select
        story.id,
        story.title,
        story.situation,
        story.task,
        story.action,
        story.result,
        1 - (story.embedding <=> query_embedding) as similarity
    from public.candidate_stories as story
    where story.user_id = filter_user_id
      and story.embedding is not null
      and 1 - (story.embedding <=> query_embedding) >= match_threshold
    order by story.embedding <=> query_embedding
    limit match_count;
$$;
