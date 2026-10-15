'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  History, 
  Search, 
  Filter, 
  ArrowRight, 
  Clock, 
  CheckCircle2, 
  XCircle, 
  Calendar 
} from 'lucide-react';
import { api } from '@/lib/api';
import { TaskDetail } from '@/types';
import { StatusBadge } from '@/components/StatusBadge';

export default function HistoryPage() {
  const [tasks, setTasks] = useState<TaskDetail[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const res = await api.getTasks({
        status: statusFilter !== 'all' ? statusFilter : undefined,
        priority: priorityFilter !== 'all' ? priorityFilter : undefined,
        search: search || undefined,
      });
      setTasks(res.tasks);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [search, statusFilter, priorityFilter]);

  return (
    <div className="space-y-8">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-semibold mb-2">
          <History className="w-3.5 h-3.5" />
          <span>Audit Ledger &amp; Provenance</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Execution History &amp; Audits</h1>
        <p className="text-sm text-slate-400 mt-1">
          Historical records of all autonomous agent workflows, deliverables, validation scores, and operator decisions.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-panel p-4 rounded-2xl border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search objectives, deliverables..."
            className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all"
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
          >
            <option value="all">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="running">Running</option>
            <option value="awaiting_approval">Awaiting Approval</option>
            <option value="paused">Paused</option>
            <option value="failed">Failed</option>
          </select>

          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
          >
            <option value="all">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-panel rounded-2xl border-slate-800 overflow-hidden">
        {isLoading ? (
          <div className="py-16 text-center text-slate-500 text-sm">Loading historical records...</div>
        ) : tasks.length === 0 ? (
          <div className="py-16 text-center text-slate-500 text-sm">No historical tasks found.</div>
        ) : (
          <div className="divide-y divide-slate-800/80">
            {tasks.map((task) => (
              <Link
                key={task.id}
                href={`/tasks/${task.id}`}
                className="group flex flex-col md:flex-row md:items-center justify-between p-5 hover:bg-slate-900/40 transition-colors gap-3"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <StatusBadge status={task.status} size="sm" />
                    <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                      {task.priority}
                    </span>
                    <span suppressHydrationWarning className="text-xs text-slate-500 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {new Date(task.created_at).toLocaleString('en-US')}
                    </span>
                  </div>
                  <h3 className="text-sm font-semibold text-white group-hover:text-indigo-400 transition-colors">
                    {task.title}
                  </h3>
                  <p className="text-xs text-slate-400 line-clamp-1">{task.objective}</p>
                </div>

                <div className="flex items-center gap-6 text-xs text-slate-400 shrink-0 self-end md:self-center">
                  {task.validation_score ? (
                    <span className="font-mono text-emerald-400 font-bold">
                      {task.validation_score}/100 Score
                    </span>
                  ) : (
                    <span className="text-slate-500">In Progress</span>
                  )}
                  <div className="flex items-center gap-1.5 text-slate-300 group-hover:text-indigo-400 font-semibold transition-colors">
                    <span>Inspect</span>
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
