# Supabase Integration & Configuration Guide

OmniAgent is fully integrated with **Supabase PostgreSQL** as its database, with asynchronous connection pooling via `asyncpg`, Supabase client support in both FastAPI and Next.js, and graceful zero-friction fallback to SQLite when live credentials are not yet configured.

---

## 1. Environment Files Created

The application now provides environment files with all required variables:

| File Location | Purpose |
|---|---|
| [`backend/.env`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/backend/.env) | Backend database credentials, Supabase keys, JWT secret, AI provider keys, CORS, limits |
| [`frontend/.env`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/frontend/.env) | Frontend public API URL, Supabase Project URL, and Supabase Anon Key |
| [`.env`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/.env) | Unified root configuration combining both frontend and backend configurations |
| [`.env.example`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/.env.example) | Sanitized template for version control |

---

## 2. Where to Find Your Supabase Credentials

1. Open your [Supabase Dashboard](https://supabase.com/dashboard).
2. Select your project (or create a new free tier project).
3. Navigate to **Project Settings** (gear icon in the sidebar) -> **API**:
   - **Project URL**: Copy into `SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_URL`.
   - **Project API Keys (`anon` / `public`)**: Copy into `SUPABASE_ANON_KEY` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
   - **Project API Keys (`service_role` / `secret`)**: Copy into `SUPABASE_SERVICE_ROLE_KEY`.
4. Navigate to **Project Settings** -> **Database**:
   - Scroll down to **Connection String** -> **URI**.
   - You can choose between:
     - **Session mode / Direct (Port 5432)**:
       ```env
       DATABASE_URL="postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"
       ```
     - **Transaction Pooler / PgBouncer (Port 6543)** *(Recommended for high concurrency & serverless)*:
       ```env
       DATABASE_URL="postgresql+asyncpg://postgres.[YOUR-PROJECT-REF]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
       ```

> [!NOTE]
> OmniAgent automatically sanitizes and adapts your `DATABASE_URL`. Even if you paste a standard `postgresql://` or `postgres://` URL copied from Supabase, [`backend/app/db/session.py`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/backend/app/db/session.py) converts it into `postgresql+asyncpg://` and configures SSL and statement caching accordingly.

---

## 3. Database Schema Migration

To apply the database schema (tasks, subtasks, agent logs, tool executions, memory, approvals) to your Supabase PostgreSQL instance:

```powershell
# In the project root with your virtual environment active:
$env:PYTHONPATH = "."
backend\venv\Scripts\python -c "import asyncio; from backend.app.db.session import init_db; asyncio.run(init_db())"
```

This executes `Base.metadata.create_all` using the configured async engine, creating all tables with foreign keys and indexes directly in your Supabase database.

---

## 4. Frontend Supabase Client

The frontend client is available in [`frontend/lib/supabase.ts`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/frontend/lib/supabase.ts):

```typescript
import { supabase } from '@/lib/supabase';

// Example: Fetching tasks directly or listening to Supabase Realtime
if (supabase) {
  const { data, error } = await supabase.from('tasks').select('*');
}
```

---

## 5. Development Fallback

If `DATABASE_URL` contains placeholder tokens like `<your-supabase-password>`, OmniAgent prints a safe diagnostic warning and automatically falls back to the local SQLite database at `backend/data/omniagent.db`. This allows the application to remain functional and testable even without an active internet connection or before credentials are provided.
