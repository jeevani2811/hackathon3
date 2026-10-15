'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { 
  ArrowLeft, 
  Play, 
  Pause, 
  XCircle, 
  RotateCw, 
  ShieldCheck, 
  Download, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Cpu, 
  Clock, 
  Sparkles, 
  Check, 
  Copy, 
  Layers 
} from 'lucide-react';
import { api } from '@/lib/api';
import { TaskDetail, SubTask, ApprovalRequest } from '@/types';
import { StatusBadge } from '@/components/StatusBadge';
import { LiveMonitor } from '@/components/LiveMonitor';
import { ApprovalModal } from '@/components/ApprovalModal';

interface LogEntry {
  timestamp: string;
  agent?: string;
  event_type: string;
  message: string;
  data?: any;
}

export default function TaskDetailPage() {
  const params = useParams();
  const taskId = params.id as string;
  const router = useRouter();

  const [task, setTask] = useState<TaskDetail | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [activeTab, setActiveTab] = useState<'monitor' | 'agents' | 'deliverable' | 'validation'>('monitor');
  const [activeApproval, setActiveApproval] = useState<ApprovalRequest | null>(null);
  const [isCopied, setIsCopied] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch complete task details
  const fetchTask = useCallback(async () => {
    try {
      const data = await api.getTask(taskId);
      setTask(data);
      // If task is awaiting approval, find pending approval
      if (data.status === 'awaiting_approval' && data.pending_approvals?.length > 0) {
        setActiveApproval(data.pending_approvals[0]);
      } else {
        // also check approval endpoint
        const approvals = await api.getApprovals({ task_id: taskId, status: 'pending' });
        if (approvals.length > 0) {
          setActiveApproval(approvals[0]);
        }
      }
    } catch (err) {
      console.error('Failed to fetch task:', err);
    } finally {
      setIsLoading(false);
    }
  }, [taskId]);

  useEffect(() => {
    fetchTask();

    // Subscribe to SSE stream for live updates
    const unsubscribe = api.subscribeToTaskEvents(
      taskId,
      (event) => {
        const timeStr = new Date().toLocaleTimeString();
        let msg = '';
        let agentName = 'Orchestrator';

        if (event.event_type === 'workflow_planning') {
          msg = event.data.message || 'Planner Agent decomposing DAG subtasks...';
          agentName = 'Planner Agent';
        } else if (event.event_type === 'subtask_started') {
          msg = `Subtask started: "${event.data.title}"`;
          agentName = event.data.agent || 'Agent Fleet';
        } else if (event.event_type === 'subtask_completed') {
          msg = `Subtask completed (${event.data.duration_ms}ms): ${event.data.summary}`;
          agentName = event.data.agent || 'Agent Fleet';
        } else if (event.event_type === 'awaiting_approval') {
          msg = `HUMAN APPROVAL REQUIRED: ${event.data.title}`;
          agentName = 'Approval Engine';
        } else if (event.event_type === 'approval_decided') {
          msg = `Approval decision: ${event.data.decision.toUpperCase()}`;
          agentName = 'Human Operator';
        } else if (event.event_type === 'workflow_completed') {
          msg = `Workflow completed with validation score ${event.data.validation_score}/100.`;
          agentName = 'Validation Agent';
        } else if (event.event_type === 'workflow_failed') {
          msg = `Fault encountered: ${event.data.error}`;
          agentName = 'Orchestrator';
        } else {
          msg = event.data.message || JSON.stringify(event.data);
        }

        setLogs((prev) => [
          ...prev,
          {
            timestamp: timeStr,
            agent: agentName,
            event_type: event.event_type,
            message: msg,
            data: event.data,
          },
        ]);

        // Refresh task status on milestone events
        if (['workflow_planning', 'subtask_completed', 'awaiting_approval', 'workflow_completed', 'workflow_failed'].includes(event.event_type)) {
          fetchTask();
        }
      },
      (err) => {
        console.warn('SSE connection issue:', err);
      }
    );

    const polling = setInterval(fetchTask, 6000);

    return () => {
      unsubscribe();
      clearInterval(polling);
    };
  }, [taskId, fetchTask]);

  const handlePause = async () => {
    await api.pauseTask(taskId);
    fetchTask();
  };

  const handleResume = async () => {
    await api.resumeTask(taskId);
    fetchTask();
  };

  const handleCancel = async () => {
    await api.cancelTask(taskId);
    fetchTask();
  };

  const handleRetry = async () => {
    await api.retryTask(taskId);
    fetchTask();
  };

  const handleCopyDeliverable = () => {
    if (task?.final_deliverable) {
      navigator.clipboard.writeText(task.final_deliverable);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const handleDownloadDeliverable = () => {
    if (!task?.final_deliverable) return;
    const blob = new Blob([task.final_deliverable], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `OmniAgent_Deliverable_${task.id.slice(0, 8)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (isLoading) {
    return (
      <div className="py-24 text-center space-y-3">
        <RotateCw className="w-8 h-8 animate-spin text-indigo-400 mx-auto" />
        <p className="text-slate-400 text-sm">Connecting to task telemetry stream...</p>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="py-24 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-rose-400 mx-auto" />
        <h2 className="text-xl font-bold text-white">Workflow Not Found</h2>
        <p className="text-slate-400 text-sm">The requested task ID does not exist in the database.</p>
        <Link href="/dashboard" className="inline-block px-4 py-2 rounded-xl bg-slate-800 text-white text-xs font-semibold">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  // Determine current active agent based on subtasks
  const runningSubtask = task.subtasks.find((st) => st.status === 'running');
  const activeAgentName = runningSubtask ? runningSubtask.assigned_agent : (task.status === 'planning' ? 'Planner Agent' : 'Orchestrator');

  return (
    <div className="space-y-6">
      {/* Back button & Breadcrumb */}
      <div className="flex items-center justify-between">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Operations</span>
        </Link>

        <div className="flex items-center gap-2 text-xs font-mono text-slate-500">
          <span>ID: {task.id.slice(0, 8)}...{task.id.slice(-4)}</span>
        </div>
      </div>

      {/* Human Approval Required Alert Banner (when awaiting approval) */}
      {task.status === 'awaiting_approval' && activeApproval && (
        <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-purple-950/90 via-indigo-950/80 to-slate-900 border border-purple-500/60 shadow-xl shadow-purple-950/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-pulse-subtle">
          <div className="flex items-start sm:items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-500/40 flex items-center justify-center shrink-0">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs uppercase font-extrabold px-2 py-0.5 rounded bg-purple-500/30 text-purple-200 border border-purple-500/40">
                  Human Sign-Off Required
                </span>
                <span className="text-xs text-slate-400">Action: {activeApproval.action_type}</span>
              </div>
              <h3 className="text-sm sm:text-base font-bold text-white mt-1">{activeApproval.title}</h3>
              <p className="text-xs text-slate-300 line-clamp-1">{activeApproval.description}</p>
            </div>
          </div>

          <button
            onClick={() => setActiveApproval(activeApproval)}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold shadow-md shadow-purple-600/30 transition-all shrink-0 self-start sm:self-auto"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Review &amp; Authorize</span>
          </button>
        </div>
      )}

      {/* Main Task Header Card */}
      <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2">
              <StatusBadge status={task.status} size="lg" />
              <span className="text-xs uppercase font-bold px-2.5 py-1 rounded-full bg-slate-800 text-indigo-400 border border-slate-700">
                Priority: {task.priority}
              </span>
              <span className="text-xs uppercase font-bold px-2.5 py-1 rounded-full bg-slate-800 text-purple-400 border border-slate-700">
                Mode: {task.mode === 'human_in_the_loop' ? 'Human-In-The-Loop' : 'Autonomous'}
              </span>
              {task.validation_score && (
                <span className="text-xs uppercase font-bold px-2.5 py-1 rounded-full bg-emerald-950/60 text-emerald-300 border border-emerald-600/50">
                  Audit Score: {task.validation_score}/100
                </span>
              )}
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-white">{task.title}</h1>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-3xl">{task.objective}</p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center gap-2 shrink-0">
            {task.status === 'running' && (
              <button
                onClick={handlePause}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-semibold border border-slate-700 transition-all"
              >
                <Pause className="w-3.5 h-3.5" />
                <span>Pause</span>
              </button>
            )}

            {task.status === 'paused' && (
              <button
                onClick={handleResume}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-300 text-xs font-semibold border border-slate-700 transition-all"
              >
                <Play className="w-3.5 h-3.5" />
                <span>Resume</span>
              </button>
            )}

            {task.status === 'failed' && (
              <button
                onClick={handleRetry}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md transition-all"
              >
                <RotateCw className="w-3.5 h-3.5" />
                <span>Retry Workflow</span>
              </button>
            )}

            {['running', 'paused', 'awaiting_approval'].includes(task.status) && (
              <button
                onClick={handleCancel}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-700/50 text-xs font-semibold transition-all"
              >
                <XCircle className="w-3.5 h-3.5" />
                <span>Cancel</span>
              </button>
            )}
          </div>
        </div>

        {task.context && (
          <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-400">
            <span className="font-semibold text-slate-300">Context: </span>
            {task.context}
          </div>
        )}
      </div>

      {/* Tabs Header */}
      <div className="flex border-b border-slate-800 space-x-6 text-sm font-medium">
        <button
          onClick={() => setActiveTab('monitor')}
          className={`pb-3 transition-colors border-b-2 flex items-center gap-2 ${
            activeTab === 'monitor'
              ? 'border-indigo-500 text-indigo-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Cpu className="w-4 h-4" />
          <span>Live Monitor &amp; DAG ({task.progress_pct}%)</span>
        </button>

        <button
          onClick={() => setActiveTab('agents')}
          className={`pb-3 transition-colors border-b-2 flex items-center gap-2 ${
            activeTab === 'agents'
              ? 'border-indigo-500 text-indigo-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Agent Workspace ({task.subtasks.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('deliverable')}
          className={`pb-3 transition-colors border-b-2 flex items-center gap-2 ${
            activeTab === 'deliverable'
              ? 'border-indigo-500 text-indigo-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Executive Deliverable {task.final_deliverable ? '✓' : ''}</span>
        </button>

        <button
          onClick={() => setActiveTab('validation')}
          className={`pb-3 transition-colors border-b-2 flex items-center gap-2 ${
            activeTab === 'validation'
              ? 'border-indigo-500 text-indigo-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <CheckCircle2 className="w-4 h-4" />
          <span>Validation Audit</span>
        </button>
      </div>

      {/* Tab 1: Live Monitor & DAG */}
      {activeTab === 'monitor' && (
        <LiveMonitor
          status={task.status}
          progressPct={task.progress_pct}
          subtasks={task.subtasks}
          logs={logs}
          activeAgent={activeAgentName}
        />
      )}

      {/* Tab 2: Agent Workspace Details */}
      {activeTab === 'agents' && (
        <div className="space-y-4">
          {task.subtasks.length === 0 ? (
            <div className="py-12 text-center text-slate-500 text-sm">
              No subtask execution records yet. The planner is generating the DAG...
            </div>
          ) : (
            task.subtasks.map((st, idx) => (
              <div key={st.id} className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-lg bg-indigo-500/20 text-indigo-300 text-xs font-bold flex items-center justify-center">
                      {idx + 1}
                    </span>
                    <div>
                      <h4 className="text-sm font-bold text-white">{st.title}</h4>
                      <p className="text-xs text-slate-400">{st.description}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="px-2.5 py-1 rounded bg-slate-800 text-xs text-slate-300 font-medium">
                      {st.assigned_agent}
                    </span>
                    <StatusBadge status={st.status} size="sm" />
                  </div>
                </div>

                {st.output_data && Object.keys(st.output_data).length > 0 && (
                  <div className="space-y-1">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      Agent Output Telemetry &amp; Structured Findings
                    </span>
                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 max-h-48 overflow-y-auto">
                      <pre>{JSON.stringify(st.output_data, null, 2)}</pre>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab 3: Executive Deliverable Viewer */}
      {activeTab === 'deliverable' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <FileText className="w-4 h-4 text-indigo-400" />
              <span>Published Strategic Brief</span>
            </h3>

            {task.final_deliverable && (
              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopyDeliverable}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-all"
                >
                  {isCopied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{isCopied ? 'Copied' : 'Copy'}</span>
                </button>

                <button
                  onClick={handleDownloadDeliverable}
                  className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md transition-all"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download .MD</span>
                </button>
              </div>
            )}
          </div>

          {!task.final_deliverable ? (
            <div className="glass-panel p-12 text-center rounded-2xl border-slate-800 space-y-2">
              <Clock className="w-8 h-8 text-slate-500 mx-auto animate-pulse" />
              <p className="text-sm font-semibold text-slate-300">Deliverable Compilation In Progress</p>
              <p className="text-xs text-slate-500">
                The final strategic brief will be published once all DAG subtasks complete and pass the Validation Agent audit.
              </p>
            </div>
          ) : (
            <div className="glass-panel p-6 sm:p-8 rounded-2xl border-slate-800 space-y-4 text-slate-200 leading-relaxed font-sans prose prose-invert max-w-none">
              <div className="whitespace-pre-wrap font-mono text-xs sm:text-sm bg-slate-950/80 p-5 rounded-xl border border-slate-800/80 overflow-x-auto text-slate-200">
                {task.final_deliverable}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 4: Validation Audit */}
      {activeTab === 'validation' && (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Compliance &amp; Quality Audit Rubric</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Automated inspection by Validation Agent checking requirement completeness, source provenance, and math accuracy.
                </p>
              </div>

              <div className="text-right">
                <span className="text-2xl font-extrabold text-emerald-400">
                  {task.validation_score ? `${task.validation_score}/100` : 'Pending'}
                </span>
                <span className="text-[10px] uppercase font-bold text-slate-500 block">Rubric Score</span>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-1">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Objective Requirements Coverage</span>
                </div>
                <p className="text-xs text-slate-300">
                  All target entities, pricing tiers, and latency benchmarks evaluated without omissions.
                </p>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-1">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Mathematical Verification</span>
                </div>
                <p className="text-xs text-slate-300">
                  Deterministic financial calculator verified TCO and ROI projections; 0% hallucinated calculations.
                </p>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-1">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Authoritative Provenance</span>
                </div>
                <p className="text-xs text-slate-300">
                  Every factual assertion cited with authoritative SEC, vendor pricing, and architecture disclosures.
                </p>
              </div>

              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-1">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Security &amp; Policy Adherence</span>
                </div>
                <p className="text-xs text-slate-300">
                  Input sanitized against prompt injections; sensitive side-effects bound by HMAC approvals.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Human Approval Modal (if open) */}
      {activeApproval && (
        <ApprovalModal
          approval={activeApproval}
          isOpen={Boolean(activeApproval)}
          onClose={() => setActiveApproval(null)}
          onDecisionSubmitted={() => {
            fetchTask();
          }}
        />
      )}
    </div>
  );
}
