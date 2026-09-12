-- 🔱 WILLOW RAIN EMPIRE: MASTER CLOUD SCHEMA v1.0 🔱
-- Run this in your Supabase SQL Editor to provision the database.

-- 1. Videos Feed (Main App Content)
create table if not exists public.videos (
    id bigserial primary key,
    title text not null,
    description text,
    video_url text not null,
    thumbnail_url text,
    creator text default 'Anthony AI',
    category text default 'For you',
    views text default '0',
    posted text default 'Just Now',
    created_at timestamp with time zone default now()
);

-- 2. Proxy Clients (Wholesale Infrastructure)
create table if not exists public.proxy_clients (
    id uuid default uuid_generate_v4() primary key,
    client_id text unique not null,
    email text not null,
    username text not null,
    password text not null,
    host_ip text not null,
    quota_gb real default 100.0,
    used_gb real default 0.0,
    is_active boolean default true,
    created_at timestamp with time zone default now()
);

-- 3. Active Feed Registry (Ghost Feed)
create table if not exists public.active_feed_registry (
    id uuid default uuid_generate_v4() primary key,
    post_token text unique not null,
    title text,
    media_url text,
    expires_at double precision,
    created_at timestamp with time zone default now()
);

-- 4. Feed Posts (Social Index)
create table if not exists public.feed_posts (
    id bigserial primary key,
    title text,
    content text,
    platform text,
    url text unique,
    metadata jsonb,
    created_at timestamp with time zone default now()
);

-- 5. Content Profiles (Page Memory)
create table if not exists public.content_profiles (
    page_id text primary key,
    niche text,
    audience_persona text,
    brand_voice text,
    visual_style_bible jsonb,
    success_memory jsonb,
    failure_memory jsonb,
    analytics_summary jsonb,
    created_at timestamp with time zone default now()
);

-- 5. Twin Logs (System Operations)
create table if not exists public.twin_logs (
    id bigserial primary key,
    node text,
    action text,
    details jsonb,
    timestamp timestamp with time zone default now()
);

-- 6. Legal Vault (Chain of Custody)
create table if not exists public.production_batches (
    id uuid default uuid_generate_v4() primary key,
    batch_month text not null,
    status text default 'pending_review',
    created_at timestamp with time zone default now(),
    review_deadline timestamp with time zone not null
);

create table if not exists public.projects (
    id uuid default uuid_generate_v4() primary key,
    batch_id uuid references public.production_batches(id) on delete cascade,
    title text not null,
    video_url text not null,
    script_manifest jsonb not null,
    status text default 'queued',
    created_at timestamp with time zone default now()
);

-- ENABLE ROW LEVEL SECURITY (RLS)
-- For development, we allow all access. In production, restrictive policies should be added.
alter table public.videos enable row level security;
alter table public.proxy_clients enable row level security;
alter table public.active_feed_registry enable row level security;
alter table public.content_profiles enable row level security;
alter table public.twin_logs enable row level security;
alter table public.production_batches enable row level security;
alter table public.projects enable row level security;

-- CREATE POLICIES (Allow all for service role / authenticated)
create policy "Allow all for authenticated" on public.videos for all using (true);
create policy "Allow all for authenticated" on public.proxy_clients for all using (true);
create policy "Allow all for authenticated" on public.active_feed_registry for all using (true);
create policy "Allow all for authenticated" on public.content_profiles for all using (true);
create policy "Allow all for authenticated" on public.twin_logs for all using (true);
create policy "Allow all for authenticated" on public.production_batches for all using (true);
create policy "Allow all for authenticated" on public.projects for all using (true);
