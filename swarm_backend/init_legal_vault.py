# --- EMPIRE LEGAL VAULT: TABLE PROVISIONING v1.0 ---
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Load env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def provision():
    print("[*] Provisioning Legal Vault Tables in Supabase...")

    # Note: Supabase Python client doesn't support 'CREATE TABLE' directly via standard API.
    # The user should ideally run the SQL provided in the 'legal_schema.sql' artifact.
    # However, we can try to use a dummy insert to see if they exist or suggest manual run.

    print("\n[!] IMPORTANT: Please run the following SQL in your Supabase SQL Editor:")
    print("""
-- 1. Monthly Batches Table
create table if not exists public.production_batches (
    id uuid default uuid_generate_v4() primary key,
    batch_month text not null,
    status text default 'pending_review',
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    review_deadline timestamp with time zone not null
);

-- 2. Projects Table
create table if not exists public.projects (
    id uuid default uuid_generate_v4() primary key,
    batch_id uuid references public.production_batches(id) on delete cascade,
    title text not null,
    video_url text not null,
    script_manifest jsonb not null,
    status text default 'queued'
);

-- 3. Signatures Table
create table if not exists public.project_signatures (
    id uuid default uuid_generate_v4() primary key,
    batch_id uuid references public.production_batches(id) on delete cascade,
    signer_name text not null,
    approval_statement text not null,
    content_hash text not null,
    signed_at timestamp with time zone default timezone('utc'::text, now()) not null,
    ip_address text
);
    """)

if __name__ == "__main__":
    provision()
