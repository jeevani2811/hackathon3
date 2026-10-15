'use client';

import React, { useEffect, useRef } from 'react';
import { 
  Terminal, 
  Cpu, 
  Wrench, 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  Zap, 
  Activity 
} from 'lucide-react';
import { SubTask, TaskStatus } from '@/types';
import { StatusBadge } from './StatusBadge';

interface LogEntry {
  timestamp: string;
  agent?: string;
  event_type: string;
  message: string;
  data?: any;
}

interface LiveMonitorProps {
  status: TaskStatus;
  progressPct: number;
  subtasks: SubTask[];
  logs: LogEntry[];
  activeAgent?: string;
}

export const LiveMonitor: React.FC<LiveMonitorProps> = ({
  status,
  progressPct,
  subtasks,
  logs,
  activeAgent = 'Orchestrator',
}) => {
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="space-y-6">
      {/* Active Agent Pulse Card */}
      <div className="glass-panel p-5 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border border-indigo-500/20">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
              <Cpu className="w-6 h-6 animate-pulse" />
            </div>
            {status === 'running' && (
              <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-emerald-500"></span>
              </span>
            )}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase font-bold tracking-wider text-slate-400">Current Execution Lead</span>
              <StatusBadge status={status} size="sm" />
            </div>
            <h4 className="text-lg font-bold text-white mt-0.5">{activeAgent}</h4>
            <p className="text-xs text-slate-400">
              {status === 'planning' && 'Formulating Directed Acyclic Graph (DAG) decomposition...'}
              {status === 'running' && 'Evaluating ready subtasks and executing authorized tools...'}
              {status === 'awaiting_approval' && 'Halted. Waiting on operator authorization...'}
              {status === 'completed' && 'Autonomous lifecycle finished with 100% verification.'}
              {status === 'paused' && 'Execution paused by operator.'}
              {status === 'failed' && 'Execution halted due to unrecoverable fault.'}
            </p>
          </div>
        </div>

        {/* Progress Gauge */}
        <div className="w-full sm:w-48 bg-slate-950 p-3 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-xs font-semibold mb-1.5">
            <span className="text-slate-400">Progress</span>
            <span className="text-indigo-400">{progressPct}%</span>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 transition-all duration-500 rounded-full"
              style={{ width: `${progressPct}%` }}
            />
          </div>
        </div>
      </div>

      {/* DAG Subtask Visual Pipeline */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800">
        <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
          <Activity className="w-4 h-4 text-indigo-400" />
          <span>Autonomous DAG Execution Pipeline</span>
        </h4>

        {subtasks.length === 0 ? (
          <div className="py-8 text-center text-slate-500 text-sm">
            Planner agent initializing subtask dependencies...
          </div>
        ) : (
          <div className="space-y-3">
            {subtasks.map((st, idx) => {
              const isRunning = st.status === 'running';
              const isDone = st.status === 'completed';
              const isAwaiting = st.status === 'awaiting_approval';

              return (
                <div
                  key={st.id}
                  className={`p-3.5 rounded-xl border transition-all flex flex-col md:flex-row md:items-center justify-between gap-3 ${
                    isRunning
                      ? 'bg-indigo-950/40 border-indigo-500/50 shadow-md shadow-indigo-500/10'
                      : isAwaiting
                      ? 'bg-purple-950/40 border-purple-500/50'
                      : isDone
                      ? 'bg-slate-900/40 border-slate-800/80'
                      : 'bg-slate-950/40 border-slate-800/40 opacity-70'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5 w-6 h-6 rounded-lg bg-slate-800 text-slate-300 flex items-center justify-center text-xs font-bold shrink-0">
                      {idx + 1}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold text-white">{st.title}</span>
                        <StatusBadge status={st.status} size="sm" />
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">{st.description}</p>
                      
                      {st.tools_assigned && st.tools_assigned.length > 0 && (
                        <div className="flex flex-wrap items-center gap-1.5 mt-2">
                          <span className="text-[10px] text-slate-500 font-semibold uppercase">Tools:</span>
                          {st.tools_assigned.map((tool) => (
                            <span
                              key={tool}
                              className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700 flex items-center gap-1"
                            >
                              <Wrench className="w-2.5 h-2.5" />
                              {tool}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-slate-400 shrink-0">
                    <span className="px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/60 font-medium text-slate-300">
                      {st.assigned_agent}
                    </span>
                    {st.duration_ms > 0 && (
                      <span className="font-mono text-emerald-400">
                        {st.duration_ms}ms
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Live Streaming Console Terminal */}
      <div className="bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
        <div className="px-4 py-2.5 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider font-mono">
              Live Real-Time Event Stream (SSE)
            </span>
          </div>
          <span className="flex items-center gap-1.5 text-[11px] text-emerald-400 font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            Connected
          </span>
        </div>

        <div className="p-4 font-mono text-xs space-y-2 max-h-72 overflow-y-auto bg-slate-950/90">
          {logs.length === 0 ? (
            <div className="text-slate-600 italic">Listening for real-time backend agent events...</div>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-2 text-slate-300 leading-relaxed">
                <span className="text-slate-500 shrink-0 select-none">[{log.timestamp}]</span>
                {log.agent && (
                  <span className="text-indigo-400 font-semibold shrink-0">
                    [{log.agent}]
                  </span>
                )}
                <span className="text-emerald-400 shrink-0">&gt;</span>
                <span className="break-words">{log.message}</span>
              </div>
            ))
          )}
          <div ref={logEndRef} />
        </div>
      </div>
    </div>
  );
};
