# OmniAgent Cloud Deployment Guide: Render & Vercel

This guide provides end-to-end instructions for deploying OmniAgent to production with:
- **Backend (Python FastAPI + Supabase)** hosted on **[Render](https://render.com)**
- **Frontend (Next.js 14 + Tailwind + TypeScript)** hosted on **[Vercel](https://vercel.com)**
- **Database (PostgreSQL + Auth + Storage)** hosted on **[Supabase](https://supabase.com)**

---

## Architecture Overview

```
+----------------------------------------------------------------+
|                        SUPABASE CLOUD                          |
|         PostgreSQL Database (Tasks, DAG, Logs, Approvals)      |
+-------------------------------+--------------------------------+
                                ^
                                | (Port 6543 / 5432 asyncpg)
                                v
+----------------------------------------------------------------+
|                        RENDER (BACKEND)                        |
|  FastAPI + Uvicorn + 5-Agent Fleet + Workflow Orchestrator     |
|  Public URL: https://omniagent-backend.onrender.com            |
+-------------------------------+--------------------------------+
                                ^
                                | HTTPS REST + Server-Sent Events (SSE)
                                v
+----------------------------------------------------------------+
|                        VERCEL (FRONTEND)                       |
|  Next.js 14 App Router + Tailwind CSS + Supabase Client        |
|  Public URL: https://omniagent.vercel.app                      |
+----------------------------------------------------------------+
```

---

## Clarification: Local Execution Commands

If you previously encountered `bash: npm: command not found` while inside the `backend/` folder:
- `backend/` is a **Python FastAPI** application (executed using `uvicorn`, not `npm`).
- `frontend/` is the **Next.js** web application (executed using `npm run dev` or `npm start`).

### To run locally:
```powershell
# Terminal 1: Start Backend (Python)
$env:PYTHONPATH = "."
backend\venv\Scripts\python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Frontend (Next.js)
cd frontend
npm run dev
```

---

## Part 1: Deploy Backend to Render

### Option A: 1-Click Blueprint Deploy (Recommended)
1. Push your repository to **GitHub**.
2. Log into your [Render Dashboard](https://dashboard.render.com).
3. Click **New +** -> **Blueprint**.
4. Select your GitHub repository.
5. Render will automatically read [`render.yaml`](file:///c:/Users/1412d/OneDrive/Desktop/hackathon3/render.yaml) from the root and configure all build/start commands and environment keys!
6. Provide your Supabase environment values when prompted in Render:
   - `DATABASE_URL`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GEMINI_API_KEY` (optional)
7. Click **Apply**. Render will build and deploy your API.

### Option B: Manual Web Service Setup
1. In Render Dashboard, click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the service settings:
   - **Name**: `omniagent-backend`
   - **Region**: Oregon (or your preferred region close to your Supabase DB)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (uses repo root)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment Variables**, add:
   ```env
   PYTHON_VERSION = 3.11.9
   PYTHONPATH = .
   DATABASE_URL = postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   SUPABASE_URL = https://[PROJECT-REF].supabase.co
   SUPABASE_ANON_KEY = [YOUR-SUPABASE-ANON-KEY]
   SUPABASE_SERVICE_ROLE_KEY = [YOUR-SUPABASE-SERVICE-ROLE-KEY]
   SUPABASE_DB_PASSWORD = [YOUR-PASSWORD]
   SECRET_KEY = [GENERATE-RANDOM-HEX-STRING]
   AI_PROVIDER = mock (or gemini)
   GEMINI_API_KEY = [YOUR-GEMINI-KEY]
   BACKEND_CORS_ORIGINS = https://*.vercel.app,http://localhost:3000
   ```
5. Click **Create Web Service**.
6. Once deployed, copy your Render public URL (e.g., `https://omniagent-backend.onrender.com`).
7. Verify it is running by opening: `https://omniagent-backend.onrender.com/api/v1/health`.

---

## Part 2: Deploy Frontend to Vercel

1. Log into your [Vercel Dashboard](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your GitHub repository.
4. In the **Configure Project** screen:
   - **Project Name**: `omniagent`
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click **Edit** and select `frontend` (Important!).
   - **Build Command**: `next build` (Default)
   - **Output Directory**: `.next` (Default)
   - **Install Command**: `npm install` (Default)
5. Expand **Environment Variables** and add:
   ```env
   NEXT_PUBLIC_API_URL = https://omniagent-backend.onrender.com/api/v1
   NEXT_PUBLIC_SUPABASE_URL = https://[PROJECT-REF].supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY = [YOUR-SUPABASE-ANON-KEY]
   ```
   *(Replace `https://omniagent-backend.onrender.com` with your actual Render URL from Part 1).*
6. Click **Deploy**.
7. Vercel will install dependencies, build the Next.js production bundle, and launch your application globally on Vercel's Edge Network (e.g., `https://omniagent.vercel.app`).

---

## Part 3: Connecting Frontend and Backend

1. When your Vercel deployment finishes, copy your live frontend domain (e.g. `https://omniagent.vercel.app`).
2. Verify that your Render backend allows CORS from your Vercel domain:
   - OmniAgent backend already includes wildcard support for `*.vercel.app` via `allow_origin_regex`.
   - Optionally, you can explicitly add `https://omniagent.vercel.app` to `BACKEND_CORS_ORIGINS` in your Render Environment Variables.
3. Open your Vercel site in your browser. You can now launch multi-agent tasks, inspect DAG scheduling, view agent logs, and perform human-in-the-loop approvals in production!
