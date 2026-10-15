'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  Play, 
  Pause, 
  XCircle, 
  Clock, 
  CheckCircle2, 
  AlertTriangle, 
  Cpu, 
  Search, 
  PlusCircle, 
  ArrowRight, 
  Filter, 
  Activity, 
  ShieldCheck,
  Sparkles 
} from 'lucide-react';
import { api } from '@/lib/api';
import { TaskDetail, TaskListResponse, AgentInfo } from '@/types';
import { StatusBadge } from '@/components/StatusBadge';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<TaskDetail[]>([]);
  const [metrics, setMetrics] = useState({
    total: 0,
    active: 0,
    completed: 0,
    failed: 0,
    pendingApprovals: 0,
  });
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const loadDashboardData = async () => {
    try {
      const [taskRes, agentRes, approvalRes] = await Promise.all([
        api.getTasks({ status: filterStatus !== 'all' ? filterStatus : undefined, search: searchQuery || undefined }),
        api.getAgents(),
        api.getApprovals({ status: 'pending' }),
      ]);

      setTasks(taskRes.tasks);
      setMetrics({
        total: taskRes.total,
        active: taskRes.active_count,
        completed: taskRes.completed_count,
        failed: taskRes.failed_count,
        pendingApprovals: approvalRes.length,
      });
      setAgents(agentRes);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 8000);
    return () => clearInterval(interval);
  }, [filterStatus, searchQuery]);

  const handlePause = async (e: React.MouseEvent, id: string) => {
    e.preventDefault();
    await api.pauseTask(id);
    loadDashboardData();
  };

  const handleResume = async (e: React.MouseEvent, id: string) => {
    e.preventDefault();
    await api.resumeTask(id);
    loadDashboardData();
  };

  const handleCancel = async (e: React.MouseEvent, id: string) => {
    e.preventDefault();
    await api.cancelTask(id);
    loadDashboardData();
  };

  return (
    <div className="space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Operations Dashboard</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time telemetry and management of autonomous multi-agent strategic workflows.
          </p>
        </div>

        <Link
          href="/tasks"
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-sm font-semibold shadow-lg shadow-indigo-600/20 transition-all self-start sm:self-auto"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Create Autonomous Task</span>
        </Link>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-400">Active Workflows</span>
            <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
              <Activity className="w-4 h-4 animate-pulse" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-white mt-3">{metrics.active}</p>
          <p className="text-xs text-slate-500 mt-1">Autonomous DAGs in execution</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-purple-500/30 bg-purple-950/10">
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-bold tracking-wider text-purple-300">Pending Approvals</span>
            <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-300 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-purple-200 mt-3">{metrics.pendingApprovals}</p>
          <p className="text-xs text-purple-400 mt-1">Sensitive operations awaiting HITL</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-400">Completed Deliverables</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-emerald-400 mt-3">{metrics.completed}</p>
          <p className="text-xs text-slate-500 mt-1">Verified strategic briefs published</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-400">Total Tasks Tracked</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
              <Cpu className="w-4 h-4" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-indigo-400 mt-3">{metrics.total}</p>
          <p className="text-xs text-slate-500 mt-1">
            {metrics.failed > 0 ? `${metrics.failed} failed/cancelled` : '100% operational success rate'}
          </p>
        </div>
      </div>

      {/* Main Grid: Workflows Table & Agent Fleet Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Workflows Table (2 cols) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Clock className="w-4 h-4 text-indigo-400" />
                <span>Active &amp; Recent Workflows</span>
              </h2>

              {/* Filters */}
              <div className="flex items-center gap-2">
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search workflows..."
                    className="pl-8 pr-3 py-1 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all w-36 sm:w-48"
                  />
                </div>

                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
                >
                  <option value="all">All States</option>
                  <option value="running">Running</option>
                  <option value="awaiting_approval">Awaiting Approval</option>
                  <option value="completed">Completed</option>
                  <option value="paused">Paused</option>
                  <option value="failed">Failed</option>
                </select>
              </div>
            </div>

            {/* Tasks List */}
            {isLoading ? (
              <div className="py-12 text-center text-slate-500 text-sm">Loading workflows...</div>
            ) : tasks.length === 0 ? (
              <div className="py-12 text-center space-y-3">
                <p className="text-slate-400 text-sm">No workflows match the selected criteria.</p>
                <Link
                  href="/tasks"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold"
                >
                  <PlusCircle className="w-3.5 h-3.5" />
                  <span>Start your first task</span>
                </Link>
              </div>
            ) : (
              <div className="divide-y divide-slate-800/80">
                {tasks.map((task) => (
                  <Link
                    key={task.id}
                    href={`/tasks/${task.id}`}
                    className="group block py-4 hover:bg-slate-900/40 -mx-5 px-5 transition-colors"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <StatusBadge status={task.status} size="sm" />
                          <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                            {task.mode === 'human_in_the_loop' ? 'HITL' : 'Auto'}
                          </span>
                          <span suppressHydrationWarning className="text-xs text-slate-500">
                            {new Date(task.created_at).toLocaleTimeString('en-US')}
                          </span>
                        </div>
                        <h3 className="text-sm font-semibold text-white group-hover:text-indigo-400 transition-colors">
                          {task.title}
                        </h3>
                        <p className="text-xs text-slate-400 line-clamp-1">{task.objective}</p>
                      </div>

                      {/* Right controls & progress */}
                      <div className="flex items-center gap-4 self-end sm:self-center shrink-0">
                        <div className="w-20 bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                          <div
                            className="bg-indigo-500 h-full rounded-full transition-all"
                            style={{ width: `${task.progress_pct}%` }}
                          />
                        </div>

                        {/* Control buttons */}
                        <div className="flex items-center gap-1">
                          {task.status === 'running' && (
                            <button
                              onClick={(e) => handlePause(e, task.id)}
                              title="Pause"
                              className="p-1 rounded text-slate-400 hover:text-amber-400 hover:bg-slate-800 transition-colors"
                            >
                              <Pause className="w-3.5 h-3.5" />
                            </button>
                          )}
                          {task.status === 'paused' && (
                            <button
                              onClick={(e) => handleResume(e, task.id)}
                              title="Resume"
                              className="p-1 rounded text-slate-400 hover:text-emerald-400 hover:bg-slate-800 transition-colors"
                            >
                              <Play className="w-3.5 h-3.5" />
                            </button>
                          )}
                          {['running', 'paused', 'awaiting_approval'].includes(task.status) && (
                            <button
                              onClick={(e) => handleCancel(e, task.id)}
                              title="Cancel"
                              className="p-1 rounded text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition-colors"
                            >
                              <XCircle className="w-3.5 h-3.5" />
                            </button>
                          )}
                          <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-indigo-400 transition-colors" />
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right: Agent Fleet Live Status (1 col) */}
        <div className="space-y-4">
          <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Cpu className="w-4 h-4 text-indigo-400" />
                <span>Agent Fleet Telemetry</span>
              </h2>
              <Link href="/agents" className="text-xs text-indigo-400 hover:underline">
                View All
              </Link>
            </div>

            <div className="space-y-3">
              {agents.map((agent) => (
                <div
                  key={agent.id}
                  className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 flex items-center justify-between gap-3"
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span className="text-xs font-semibold text-white">{agent.name}</span>
                    </div>
                    <p className="text-[11px] text-slate-400">{agent.role}</p>
                  </div>

                  <div className="text-right">
                    <span className="text-xs font-mono font-bold text-indigo-400">
                      {agent.successful_tasks}
                    </span>
                    <span className="text-[10px] text-slate-500 block">runs</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Pre-Built Task Card */}
          <div className="glass-panel p-5 rounded-2xl border-indigo-500/20 bg-gradient-to-b from-indigo-950/20 to-slate-900/60 space-y-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Recommended Workflow</span>
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Launch our featured autonomous vector database evaluation across Pinecone, Weaviate, and Qdrant with deterministic financial TCO modeling.
            </p>
            <Link
              href="/tasks?template=tpl-vector-db"
              className="inline-flex items-center gap-1.5 w-full justify-center px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md transition-all"
            >
              <span>Load Template in Studio</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
