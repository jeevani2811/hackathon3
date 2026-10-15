'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  Cpu, 
  Layers, 
  Calculator, 
  CheckCircle2, 
  Workflow, 
  Database, 
  FileCheck2, 
  Zap, 
  TrendingUp, 
  Lock 
} from 'lucide-react';

export default function LandingPage() {
  // Interactive ROI Calculator State
  const [analysts, setAnalysts] = useState(5);
  const [hoursPerWeek, setHoursPerWeek] = useState(15);
  const [hourlyRate, setHourlyRate] = useState(95);

  const annualManualCost = analysts * hoursPerWeek * 50 * hourlyRate;
  const annualOmniAgentCost = 12000; // Flat platform tier
  const annualSavings = Math.max(0, annualManualCost - annualOmniAgentCost);
  const roiMultiplier = Math.round((annualSavings / annualOmniAgentCost) * 10) / 10;

  return (
    <div className="space-y-24 py-6">
      {/* Hero Section */}
      <section className="relative text-center space-y-6 pt-10 pb-8 overflow-hidden">
        {/* Glow backdrop */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-indigo-600/15 blur-[120px] rounded-full pointer-events-none -z-10" />

        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-500/30 text-xs font-semibold text-indigo-300">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span>Next-Generation Multi-Agent Strategic Intelligence</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-[1.15]">
          Autonomous Strategic Analysis for <span className="gradient-text">High-Stakes Decisions</span>
        </h1>

        <p className="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Replace weeks of fragmented manual research with a collaborative multi-agent fleet that gathers verified evidence, computes deterministic financial TCO, and enforces strict human-in-the-loop approvals.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/tasks"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-base shadow-lg shadow-indigo-600/30 hover:shadow-indigo-600/50 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <span>Launch Live Autonomous Task</span>
            <ArrowRight className="w-5 h-5" />
          </Link>

          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-semibold text-base transition-all"
          >
            <span>View Live Dashboard</span>
          </Link>
        </div>

        {/* Feature Badges */}
        <div className="pt-8 flex flex-wrap items-center justify-center gap-6 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Zero Hallucinated Financial Math</span>
          </div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            <span>Cryptographic HMAC Approval Gates</span>
          </div>
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-purple-400" />
            <span>Sub-Second SSE Event Streaming</span>
          </div>
        </div>
      </section>

      {/* Problem vs Solution Grid */}
      <section className="space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">The Paradigm Shift</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-white">Why Conventional Chatbots Fall Short</h2>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Traditional AI chatbots hallucinate numbers, lack durable state, and cannot coordinate specialized tasks or seek permission for critical writes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* The Pain Point */}
          <div className="glass-panel p-6 sm:p-8 rounded-2xl border-rose-500/20 bg-gradient-to-b from-rose-950/20 to-slate-900/60 space-y-5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs font-bold uppercase tracking-wider">
              Traditional Fragmented Workflows
            </div>
            <ul className="space-y-4 text-sm text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0">✕</span>
                <span><strong>Hallucinated Figures:</strong> LLMs generate plausible-sounding but mathematically false ROI and pricing estimates.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0">✕</span>
                <span><strong>No Human Oversight:</strong> Either completely unguided autonomous execution with destructive side-effects, or static chat boxes.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0">✕</span>
                <span><strong>Monolithic Prompting:</strong> A single prompt tries to plan, research, calculate, and format—failing at subtle edge cases.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-rose-400 font-bold shrink-0">✕</span>
                <span><strong>Ephemeral Memory:</strong> Lost context between steps with no audit trail or persistent compliance records.</span>
              </li>
            </ul>
          </div>

          {/* The OmniAgent Solution */}
          <div className="glass-panel p-6 sm:p-8 rounded-2xl border-indigo-500/30 bg-gradient-to-b from-indigo-950/20 to-slate-900/60 space-y-5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-bold uppercase tracking-wider">
              The OmniAgent Architecture
            </div>
            <ul className="space-y-4 text-sm text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓</span>
                <span><strong>Deterministic Tooling:</strong> Mathematical calculations run via deterministic AST code, never LLM guesswork.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓</span>
                <span><strong>Cryptographic HITL Controls:</strong> Sensitive DB writes or external webhooks pause execution and require HMAC sign-off.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓</span>
                <span><strong>Specialized 5-Agent Fleet:</strong> Planner, Research, Execution, Analysis, and Validation Agents execute bounded contracts.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 font-bold shrink-0">✓</span>
                <span><strong>Durable State &amp; SSE:</strong> Complete DAG state machine persisted to SQLite/PostgreSQL with live progress streaming.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Multi-Agent Fleet Interactive Showcase */}
      <section className="space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Collaborative Fleet</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-white">5 Specialized Agents, One Orchestrated System</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* Planner */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 hover:border-indigo-500/40 transition-all hover:-translate-y-1">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold mb-4">
              01
            </div>
            <h3 className="text-base font-bold text-white">Planner Agent</h3>
            <p className="text-xs font-medium text-indigo-400 mb-2">DAG Decomposition &amp; Constraints</p>
            <p className="text-xs text-slate-400 leading-relaxed">
              Decomposes user objectives into a Directed Acyclic Graph (DAG) with explicit dependency ordering and token budget estimation.
            </p>
          </div>

          {/* Research */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 hover:border-indigo-500/40 transition-all hover:-translate-y-1">
            <div className="w-10 h-10 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold mb-4">
              02
            </div>
            <h3 className="text-base font-bold text-white">Research Agent</h3>
            <p className="text-xs font-medium text-blue-400 mb-2">Verified Sourcing &amp; Ingestion</p>
            <p className="text-xs text-slate-400 leading-relaxed">
              Scrapes verified SEC and technical databases, ingests architecture specs, and flags assumptions vs. verified facts.
            </p>
          </div>

          {/* Execution */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 hover:border-indigo-500/40 transition-all hover:-translate-y-1">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold mb-4">
              03
            </div>
            <h3 className="text-base font-bold text-white">Execution Agent</h3>
            <p className="text-xs font-medium text-emerald-400 mb-2">Deterministic Computation &amp; Tools</p>
            <p className="text-xs text-slate-400 leading-relaxed">
              Executes strictly bounded registered tools: multi-year TCO calculations, matrix transformers, deliverable generation, and webhook alerts.
            </p>
          </div>

          {/* Analysis */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 hover:border-indigo-500/40 transition-all hover:-translate-y-1">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold mb-4">
              04
            </div>
            <h3 className="text-base font-bold text-white">Analysis Agent</h3>
            <p className="text-xs font-medium text-purple-400 mb-2">SWOT Moats &amp; Threat Scoring</p>
            <p className="text-xs text-slate-400 leading-relaxed">
              Synthesizes qualitative evidence with quantitative models, identifies vendor lock-in vulnerabilities, and builds actionable strategy briefs.
            </p>
          </div>

          {/* Validation */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 hover:border-indigo-500/40 transition-all hover:-translate-y-1">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold mb-4">
              05
            </div>
            <h3 className="text-base font-bold text-white">Validation Agent</h3>
            <p className="text-xs font-medium text-amber-400 mb-2">Compliance Rubric &amp; Feedback</p>
            <p className="text-xs text-slate-400 leading-relaxed">
              Audits deliverables against prompt constraints, verifies math accuracy, assigns 0-100 rubric scores, and loops for bounded corrections.
            </p>
          </div>

          {/* Orchestrator */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 hover:border-indigo-500/40 transition-all hover:-translate-y-1">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold mb-4">
              06
            </div>
            <h3 className="text-base font-bold text-white">Workflow Orchestrator</h3>
            <p className="text-xs font-medium text-cyan-400 mb-2">State Machine &amp; HITL Interceptor</p>
            <p className="text-xs text-slate-400 leading-relaxed">
              Schedules parallel tasks in the DAG, intercepts sensitive actions for operator approval, and broadcasts SSE streaming events.
            </p>
          </div>
        </div>
      </section>

      {/* Interactive ROI Calculator */}
      <section className="glass-panel p-8 sm:p-10 rounded-3xl border border-indigo-500/30 bg-gradient-to-br from-indigo-950/30 via-slate-900 to-slate-950">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="text-center space-y-2">
            <span className="text-xs uppercase font-bold tracking-widest text-indigo-400 flex items-center justify-center gap-1.5">
              <Calculator className="w-4 h-4" />
              <span>Interactive ROI Calculator</span>
            </span>
            <h2 className="text-3xl font-bold text-white">Quantify Your Operational Time &amp; Cost Savings</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
            {/* Slider 1 */}
            <div className="space-y-2 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-400">Strategy Analysts:</span>
                <span className="text-indigo-400 font-bold">{analysts}</span>
              </div>
              <input
                type="range"
                min="1"
                max="25"
                value={analysts}
                onChange={(e) => setAnalysts(parseInt(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>

            {/* Slider 2 */}
            <div className="space-y-2 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-400">Manual Hours / Wk:</span>
                <span className="text-indigo-400 font-bold">{hoursPerWeek} hrs</span>
              </div>
              <input
                type="range"
                min="5"
                max="35"
                value={hoursPerWeek}
                onChange={(e) => setHoursPerWeek(parseInt(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>

            {/* Slider 3 */}
            <div className="space-y-2 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-400">Blended Hourly Rate:</span>
                <span className="text-indigo-400 font-bold">${hourlyRate}/hr</span>
              </div>
              <input
                type="range"
                min="50"
                max="250"
                step="5"
                value={hourlyRate}
                onChange={(e) => setHourlyRate(parseInt(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>
          </div>

          {/* Results Display */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 text-center">
            <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
              <p className="text-xs text-slate-400 font-medium">Manual Research Run-Rate</p>
              <p suppressHydrationWarning className="text-2xl font-extrabold text-slate-300 mt-1">
                ${annualManualCost.toLocaleString('en-US')} <span className="text-xs font-normal">/yr</span>
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-indigo-950/50 border border-indigo-500/40">
              <p className="text-xs text-indigo-300 font-medium">Projected Annual Savings</p>
              <p suppressHydrationWarning className="text-2xl font-extrabold text-emerald-400 mt-1">
                ${annualSavings.toLocaleString('en-US')} <span className="text-xs font-normal">/yr</span>
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-purple-950/50 border border-purple-500/40">
              <p className="text-xs text-purple-300 font-medium">Annualized ROI</p>
              <p className="text-2xl font-extrabold text-purple-300 mt-1">
                {roiMultiplier}x <span className="text-xs font-normal">Return</span>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Ready to Deploy CTA */}
      <section className="text-center space-y-5 py-12">
        <h2 className="text-3xl sm:text-4xl font-bold text-white">Experience Autonomous Strategic Operations</h2>
        <p className="text-sm text-slate-400 max-w-lg mx-auto">
          Start a pre-built SaaS Vector Database benchmark or create your own custom multi-agent workflow in seconds.
        </p>
        <Link
          href="/tasks"
          className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-base shadow-xl shadow-indigo-600/30 transition-all hover:scale-105"
        >
          <span>Get Started in Task Studio</span>
          <ArrowRight className="w-5 h-5" />
        </Link>
      </section>
    </div>
  );
}
