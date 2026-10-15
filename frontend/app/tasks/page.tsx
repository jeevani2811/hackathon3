'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  Zap, 
  Sliders, 
  Layers, 
  AlertTriangle, 
  CheckCircle2, 
  FileText 
} from 'lucide-react';
import { api } from '@/lib/api';

const PREBUILT_TEMPLATES = [
  {
    id: 'tpl-vector-db',
    title: 'Deep-Dive SaaS Vector Database Disruption & Moat Analysis',
    priority: 'high',
    mode: 'human_in_the_loop',
    objective: 'Analyze top 3 enterprise vector database providers: Pinecone, Weaviate, and Qdrant. Compare on p99 query latency, multi-cloud availability, serverless pricing curves, SOC2 compliance, and enterprise moats.',
    context: 'Evaluating migration for a high-growth fintech platform. Critical requirements: p99 latency under 20ms at 12M monthly queries, 350GB vector dataset, multi-cloud disaster recovery, and SOC2 Type II certification.',
    badge: 'Featured Demo'
  },
  {
    id: 'tpl-hyperscaler-ai',
    title: 'Hyperscaler LLM Gateway & Enterprise Cloud Benchmark',
    priority: 'critical',
    mode: 'autonomous',
    objective: 'Benchmark AWS Bedrock, Azure OpenAI Service, and Google Cloud Vertex AI on token rate limits, regional failover, HIPAA compliance, and 3-year TCO projections.',
    context: 'Consolidating LLM inference gateways for enterprise healthcare workloads. High-volume document summarization pipeline processing 50M tokens weekly.',
    badge: 'Enterprise Cloud'
  },
  {
    id: 'tpl-identity-consolidation',
    title: 'Zero-Trust Identity & Access Management (IAM) Vendor Audit',
    priority: 'medium',
    mode: 'human_in_the_loop',
    objective: 'Evaluate Okta, Microsoft Entra ID, and CyberArk on conditional access policy ergonomics, per-seat licensing cost models, and migration payback period.',
    context: 'Enterprise corporate consolidation across 4,500 active employees. Current multi-vendor sprawl costs $45,000 monthly.',
    badge: 'Cybersecurity'
  }
];

export default function TaskCreationPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [title, setTitle] = useState('');
  const [objective, setObjective] = useState('');
  const [context, setContext] = useState('');
  const [priority, setPriority] = useState('high');
  const [mode, setMode] = useState('human_in_the_loop');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const tplParam = searchParams.get('template') || 'tpl-vector-db';
    const found = PREBUILT_TEMPLATES.find((t) => t.id === tplParam) || PREBUILT_TEMPLATES[0];
    if (found) {
      setTitle(found.title);
      setObjective(found.objective);
      setContext(found.context);
      setPriority(found.priority);
      setMode(found.mode);
    }
  }, [searchParams]);

  const handleSelectTemplate = (tpl: typeof PREBUILT_TEMPLATES[0]) => {
    setTitle(tpl.title);
    setObjective(tpl.objective);
    setContext(tpl.context);
    setPriority(tpl.priority);
    setMode(tpl.mode);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (title.trim().length < 3) {
      setError('Title must be at least 3 characters.');
      return;
    }
    if (objective.trim().length < 10) {
      setError('Objective must be at least 10 characters detailing the task goals.');
      return;
    }

    setIsSubmitting(true);
    try {
      const task = await api.createTask({
        title,
        objective,
        context,
        priority,
        mode,
      });
      // Redirect to the live execution monitor page
      router.push(`/tasks/${task.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to initiate workflow.');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Task Planning Studio</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Initiate Autonomous Workflow</h1>
        <p className="text-sm text-slate-400 mt-1">
          Define your strategic objective. The multi-agent orchestrator will decompose your goal into a verifiable DAG, gather verified citations, and compile an audit-ready executive brief.
        </p>
      </div>

      {/* Pre-built Templates Carousel / Grid */}
      <div className="space-y-3">
        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
          Select an Enterprise Workflow Template (Or Customize Below)
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {PREBUILT_TEMPLATES.map((tpl) => {
            const isSelected = title === tpl.title;
            return (
              <button
                key={tpl.id}
                type="button"
                onClick={() => handleSelectTemplate(tpl)}
                className={`p-4 rounded-xl border text-left transition-all relative ${
                  isSelected
                    ? 'bg-indigo-950/50 border-indigo-500 shadow-md shadow-indigo-500/20'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900'
                }`}
              >
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  {tpl.badge}
                </span>
                <h3 className="text-sm font-semibold text-white mt-2 line-clamp-2">{tpl.title}</h3>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{tpl.objective}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Creation Form */}
      <form onSubmit={handleSubmit} className="glass-panel p-6 sm:p-8 rounded-2xl border-slate-800 space-y-6">
        {error && (
          <div className="p-4 bg-rose-950/50 border border-rose-600/50 rounded-xl text-rose-300 text-sm flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="space-y-1.5">
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Workflow Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Deep-Dive SaaS Vector Database Disruption & Moat Analysis"
            required
            className="w-full px-4 py-3 bg-slate-950 border border-slate-800 focus:border-indigo-500 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all font-medium"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Primary Strategic Objective &amp; Requirements
          </label>
          <textarea
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            rows={4}
            placeholder="Describe what the agent fleet must accomplish. Specify vendors, benchmarks, SLAs, and requirements..."
            required
            className="w-full px-4 py-3 bg-slate-950 border border-slate-800 focus:border-indigo-500 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all leading-relaxed"
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Technical Constraints &amp; Operational Context (Optional)
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            rows={3}
            placeholder="Specific corporate constraints: compliance standards (SOC2, HIPAA), target budget limits, engineering rates, volume SLAs..."
            className="w-full px-4 py-3 bg-slate-950 border border-slate-800 focus:border-indigo-500 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all leading-relaxed"
          />
        </div>

        {/* Configuration Selectors */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2">
          {/* Priority */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Execution Priority
            </label>
            <div className="grid grid-cols-4 gap-2">
              {['low', 'medium', 'high', 'critical'].map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setPriority(p)}
                  className={`py-2 rounded-xl text-xs font-bold uppercase tracking-wider border transition-all ${
                    priority === p
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/30'
                      : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          {/* Mode */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Oversight Governance Model
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setMode('human_in_the_loop')}
                className={`py-2 px-3 rounded-xl text-xs font-bold uppercase tracking-wider border flex items-center justify-center gap-1.5 transition-all ${
                  mode === 'human_in_the_loop'
                    ? 'bg-purple-900/60 text-purple-200 border-purple-500 shadow-md shadow-purple-500/20'
                    : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700'
                }`}
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Human-In-The-Loop</span>
              </button>

              <button
                type="button"
                onClick={() => setMode('autonomous')}
                className={`py-2 px-3 rounded-xl text-xs font-bold uppercase tracking-wider border flex items-center justify-center gap-1.5 transition-all ${
                  mode === 'autonomous'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/30'
                    : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700'
                }`}
              >
                <Zap className="w-3.5 h-3.5" />
                <span>Autonomous</span>
              </button>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4 flex items-center justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-base font-bold shadow-xl shadow-indigo-600/30 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
          >
            <span>{isSubmitting ? 'Initializing Agent Fleet...' : 'Deploy Autonomous Workflow'}</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
}
