# OmniAgent: Demonstration Walkthrough & Video Script

**Target Duration:** 4 minutes 30 seconds  
**Demo Persona:** Enterprise Corporate Strategy Lead / Principal Architecture Analyst  
**Focus Use Case:** Autonomous Competitive Intelligence & Financial TCO Evaluation for SaaS Vector Databases  

---

## Timeline & Narration Script

### Scene 1: The Problem & System Overview (0:00 – 0:45)
- **Visual:** Landing Page (`/`), scrolling through the Problem vs. Solution breakdown and interactive ROI calculator.
- **Narrator Audio:**
  > *"Welcome to OmniAgent. Modern enterprise strategy teams spend upwards of 15 hours every week manually collecting fragmented market data, checking vendor pricing sheets, and guessing at multi-year TCO. Standard chatbots hallucinate math, lack persistent state, and cannot coordinate specialized tasks.*
  > 
  > *OmniAgent is a full-stack, autonomous multi-agent operational platform. It combines a 5-agent collaborative fleet with deterministic computational tools, real-time Server-Sent Events, and cryptographic human-in-the-loop governance for sensitive operations."*

---

### Scene 2: Task Studio & Autonomous Goal Definition (0:45 – 1:30)
- **Visual:** Click **"New Task"** or navigate to `/tasks`. Select the **"Deep-Dive SaaS Vector Database Disruption & Moat Analysis"** pre-built template. Show the objective, technical constraints (SOC2, p99 latency < 20ms, 12M monthly queries), and select **Human-In-The-Loop** mode.
- **Narrator Audio:**
  > *"In our Task Studio, we initiate a high-stakes evaluation: analyzing Pinecone, Weaviate, and Qdrant for a Series-B fintech migration. Notice we select 'Human-in-the-loop' mode so that sensitive actions require operator sign-off. We deploy the workflow."*
- **Action:** Click **"Deploy Autonomous Workflow"**. Redirects instantly to `/tasks/[id]`.

---

### Scene 3: Live DAG Orchestration & SSE Stream (1:30 – 2:30)
- **Visual:** Live Execution Monitor (`/tasks/[id]`). Show the Planner Agent formulating the 5-step DAG. Observe the streaming terminal logs via SSE. Subtask 1 (Ingest Parameters) and Subtask 2 (Gather Competitive Market Evidence) execute, showing real-time agent pulses and tool duration in milliseconds.
- **Narrator Audio:**
  > *"Immediately, the Planner Agent inspects our objective, extracts technical constraints, and establishes a Directed Acyclic Graph (DAG) with explicit dependencies. Through Server-Sent Events, we watch the live telemetry stream. The Research Agent ingests factual disclosures and queries authorized SEC sources, tagging verified facts and assumptions with confidence ratings."*

---

### Scene 4: Human-in-the-Loop Approval Gate (2:30 – 3:15)
- **Visual:** Workflow halts in `awaiting_approval`. A glowing purple banner appears: **"Human Sign-Off Required"**. Click **"Review & Authorize"**. Inspect the modal displaying proposed parameters, reason, and cryptographic HMAC-SHA256 signature hash.
- **Narrator Audio:**
  > *"Now observe our safety governance model in action. The Execution Agent is tasked with writing corporate battlecards to our enterprise database. Because this is classified as a sensitive side-effect, the orchestrator safely pauses the workflow.*
  > 
  > *In the review dialog, we inspect the exact parameters, the cryptographic HMAC signature binding the action to this task version, and we authorize execution."*
- **Action:** Click **"Approve Execution"**. The modal closes and the DAG seamlessly resumes execution.

---

### Scene 5: Deterministic Math, SWOT & Validation (3:15 – 4:15)
- **Visual:** Switch tabs to **"Executive Deliverable"** and **"Validation Audit"**. Highlight the non-hallucinated financial calculations (Pinecone vs. Weaviate vs. Qdrant 1-yr and 3-yr TCO), the competitive capability matrix, and the 96/100 validation audit rubric score.
- **Narrator Audio:**
  > *"Notice Section 3 of our executive brief: this financial TCO model wasn't hallucinated by an LLM prompt. It was deterministically calculated by our execution engine using verifiable pricing formulas, factoring in read/write units, storage gigabytes, and engineering maintenance.*
  > 
  > *Finally, the Validation Agent audited the deliverable against our initial constraints, awarding a 96.5/100 compliance rubric score before compiling the final Markdown deliverable."*
- **Action:** Click **"Download .MD"** and show the downloaded file.

---

### Scene 6: Architecture & Operational Diagnostics (4:15 – 4:45)
- **Visual:** Navigate to `/agents` to show the agent fleet telemetry, then `/settings` to show the live diagnostics and provider switcher (Mock Engine, Gemini, OpenAI).
- **Narrator Audio:**
  > *"Under the hood, OmniAgent runs on FastAPI, SQLAlchemy, and Next.js App Router, with complete provider abstraction supporting Google Gemini, OpenAI, Anthropic, or our offline deterministic engine. This is real agentic AI: autonomous, verifiable, and enterprise-ready."*

---

## Demo Checklist for Presenters

1. Start backend: `python -m uvicorn backend.app.main:app --port 8000`
2. Start frontend: `npm run dev` in `frontend/` (port 3000)
3. Open browser at `http://localhost:3000`
4. Confirm health indicator says **"Engine Online"**
5. Follow script steps above.
