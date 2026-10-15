'use client';

import React, { useEffect, useState } from 'react';
import { 
  Settings, 
  Cpu, 
  ShieldCheck, 
  CheckCircle2, 
  Sliders, 
  Save, 
  AlertTriangle, 
  Activity, 
  Lock 
} from 'lucide-react';
import { api } from '@/lib/api';
import { SystemSettings, SystemHealth } from '@/types';

export default function SettingsPage() {
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [provider, setProvider] = useState('mock');
  const [geminiKey, setGeminiKey] = useState('');
  const [openaiKey, setOpenaiKey] = useState('');
  const [maxSubtasks, setMaxSubtasks] = useState(15);
  const [maxRetries, setMaxRetries] = useState(3);
  const [autoApproveSafe, setAutoApproveSafe] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [s, h] = await Promise.all([api.getSettings(), api.getHealth()]);
        setSettings(s);
        setHealth(h);
        setProvider(s.ai_provider);
        setMaxSubtasks(s.max_subtasks);
        setMaxRetries(s.max_retries);
        setAutoApproveSafe(s.auto_approve_safe_tools);
      } catch (err) {
        console.error('Failed to load settings:', err);
      }
    };
    load();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setStatusMessage(null);

    try {
      const updated = await api.updateSettings({
        ai_provider: provider,
        gemini_configured: geminiKey ? true : undefined,
        openai_configured: openaiKey ? true : undefined,
        max_subtasks: maxSubtasks,
        max_retries: maxRetries,
        auto_approve_safe_tools: autoApproveSafe,
      });
      setSettings(updated);
      setStatusMessage('Settings updated successfully.');
      setTimeout(() => setStatusMessage(null), 3000);
    } catch (err: any) {
      setStatusMessage(`Error: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-semibold mb-2">
          <Settings className="w-3.5 h-3.5" />
          <span>System Configuration</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">System &amp; AI Provider Settings</h1>
        <p className="text-sm text-slate-400 mt-1">
          Configure model providers, API credentials, autonomous execution budgets, and governance thresholds.
        </p>
      </div>

      {/* Diagnostics Card */}
      <div className="glass-panel p-5 rounded-2xl border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <Activity className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">System Diagnostics &amp; Health</h3>
            <p className="text-xs text-slate-400">
              Database: <span className="text-emerald-400 font-medium">{health?.database_connected ? 'Connected' : 'Disconnected'}</span> | Uptime: {health?.uptime_seconds}s
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
            RAM: {health?.system_metrics.ram_usage_pct}%
          </span>
          <span className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-indigo-400 font-bold uppercase">
            Active: {settings?.ai_provider}
          </span>
        </div>
      </div>

      {statusMessage && (
        <div className="p-4 bg-emerald-950/60 border border-emerald-600/50 rounded-xl text-emerald-300 text-sm flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Main Settings Form */}
      <form onSubmit={handleSave} className="glass-panel p-6 sm:p-8 rounded-2xl border-slate-800 space-y-6">
        {/* Provider Switcher */}
        <div className="space-y-3">
          <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
            Primary Model Provider
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
            {[
              { id: 'mock', name: 'Deterministic Engine', desc: 'Zero API keys required. High-fidelity responses.' },
              { id: 'gemini', name: 'Google Gemini', desc: 'gemini-1.5-flash with structured JSON output.' },
              { id: 'openai', name: 'OpenAI GPT-4o', desc: 'gpt-4o-mini structured reasoning API.' },
              { id: 'anthropic', name: 'Anthropic Claude', desc: 'Claude 3.5 Sonnet / Haiku integration.' },
            ].map((p) => {
              const isSelected = provider === p.id;
              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setProvider(p.id)}
                  className={`p-4 rounded-xl border text-left transition-all ${
                    isSelected
                      ? 'bg-indigo-950/50 border-indigo-500 shadow-md shadow-indigo-500/20'
                      : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-white">{p.name}</span>
                    {isSelected && <span className="w-2 h-2 rounded-full bg-indigo-400" />}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{p.desc}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* API Credentials */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-slate-500" />
              <span>Gemini API Key</span>
            </label>
            <input
              type="password"
              value={geminiKey}
              onChange={(e) => setGeminiKey(e.target.value)}
              placeholder={settings?.gemini_configured ? '•••••••••••••••• (Configured)' : 'Enter GEMINI_API_KEY...'}
              className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-mono"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-slate-500" />
              <span>OpenAI API Key</span>
            </label>
            <input
              type="password"
              value={openaiKey}
              onChange={(e) => setOpenaiKey(e.target.value)}
              placeholder={settings?.openai_configured ? '•••••••••••••••• (Configured)' : 'Enter OPENAI_API_KEY...'}
              className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-mono"
            />
          </div>
        </div>

        {/* Execution Budget Controls */}
        <div className="pt-4 border-t border-slate-800/80 space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Sliders className="w-4 h-4 text-indigo-400" />
            <span>Execution Budgets &amp; Safety Controls</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-400">Max Subtasks Per Plan</label>
              <input
                type="number"
                min="3"
                max="30"
                value={maxSubtasks}
                onChange={(e) => setMaxSubtasks(parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white font-mono"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-400">Bounded Retries on Fault</label>
              <input
                type="number"
                min="1"
                max="5"
                value={maxRetries}
                onChange={(e) => setMaxRetries(parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white font-mono"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-400">Auto-Approve Safe Tools</label>
              <div className="pt-1">
                <label className="inline-flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={autoApproveSafe}
                    onChange={(e) => setAutoApproveSafe(e.target.checked)}
                    className="w-4 h-4 rounded accent-indigo-500"
                  />
                  <span className="text-xs text-slate-300">Allow read-only tools to run without pause</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="pt-4 flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-bold shadow-md shadow-indigo-600/20 transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{isSaving ? 'Saving Changes...' : 'Save Configuration'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
