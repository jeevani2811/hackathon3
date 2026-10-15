'use client';

import React, { useEffect, useState } from 'react';
import { 
  Cpu, 
  Wrench, 
  FileCode, 
  CheckCircle2, 
  Activity, 
  Clock, 
  Layers, 
  ShieldCheck 
} from 'lucide-react';
import { api } from '@/lib/api';
import { AgentInfo } from '@/types';

export default function AgentsPage() {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<AgentInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await api.getAgents();
        setAgents(data);
        if (data.length > 0) setSelectedAgent(data[0]);
      } catch (err) {
        console.error('Failed to load agents:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchAgents();
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-semibold mb-2">
          <Cpu className="w-3.5 h-3.5" />
          <span>Multi-Agent Fleet Architecture</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Agent Fleet Workspace</h1>
        <p className="text-sm text-slate-400 mt-1">
          Inspect specialized agent specifications, system prompt instructions, assigned tools, and execution metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Agent Cards List */}
        <div className="space-y-3">
          {agents.map((agent) => {
            const isSelected = selectedAgent?.id === agent.id;
            return (
              <button
                key={agent.id}
                onClick={() => setSelectedAgent(agent)}
                className={`w-full p-4 rounded-2xl border text-left transition-all ${
                  isSelected
                    ? 'bg-indigo-950/50 border-indigo-500 shadow-md shadow-indigo-500/20'
                    : 'glass-panel border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <h3 className="text-sm font-bold text-white">{agent.name}</h3>
                  </div>
                  <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-slate-800 text-indigo-400">
                    {agent.role.split(' ')[0]}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1">{agent.role}</p>

                <div className="mt-3 flex items-center justify-between text-xs text-slate-500 font-mono border-t border-slate-800/80 pt-2">
                  <span>{agent.total_tasks_executed} tasks executed</span>
                  <span className="text-emerald-400">{agent.avg_duration_ms}ms avg</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Right: Selected Agent Detail Spec */}
        <div className="lg:col-span-2">
          {selectedAgent ? (
            <div className="glass-panel p-6 sm:p-8 rounded-2xl border-slate-800 space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-5">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                    <h2 className="text-xl font-bold text-white">{selectedAgent.name}</h2>
                    <span className="text-xs uppercase font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      Active Lead
                    </span>
                  </div>
                  <p className="text-sm text-indigo-400 font-medium mt-0.5">{selectedAgent.role}</p>
                </div>

                <div className="flex items-center gap-4 text-xs font-mono">
                  <div className="text-right">
                    <span className="text-white font-bold block">{selectedAgent.total_tasks_executed}</span>
                    <span className="text-slate-500 text-[10px]">TOTAL RUNS</span>
                  </div>
                  <div className="text-right">
                    <span className="text-emerald-400 font-bold block">100%</span>
                    <span className="text-slate-500 text-[10px]">SUCCESS</span>
                  </div>
                </div>
              </div>

              {/* Responsibilities */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
                  Agent Mandate &amp; Responsibilities
                </label>
                <p className="text-sm text-slate-200 bg-slate-950/60 p-4 rounded-xl border border-slate-800 leading-relaxed">
                  {selectedAgent.description}
                </p>
              </div>

              {/* Authorized Tools */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
                  Authorized Capability Tools
                </label>
                {selectedAgent.authorized_tools.length === 0 ? (
                  <p className="text-xs text-slate-500 italic">Pure reasoning agent; does not invoke external tools.</p>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {selectedAgent.authorized_tools.map((tool) => (
                      <span
                        key={tool}
                        className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-indigo-300 flex items-center gap-1.5"
                      >
                        <Wrench className="w-3.5 h-3.5" />
                        <span>{tool}</span>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* System Instructions / Prompt */}
              <div className="space-y-2">
                <div className="flex items-center gap-1.5 text-xs font-bold text-slate-400 uppercase tracking-wider">
                  <FileCode className="w-4 h-4 text-indigo-400" />
                  <span>Agent System Instruction Contract</span>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto whitespace-pre-wrap max-h-56">
                  {selectedAgent.system_prompt}
                </div>
              </div>
            </div>
          ) : (
            <div className="glass-panel p-12 text-center rounded-2xl border-slate-800 text-slate-500">
              Select an agent from the list to view its configuration.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
