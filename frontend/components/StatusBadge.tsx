import React from 'react';
import { TaskStatus } from '@/types';
import { 
  Clock, 
  RotateCw, 
  AlertTriangle, 
  Play, 
  Pause, 
  CheckCircle2, 
  XCircle, 
  Ban 
} from 'lucide-react';

interface StatusBadgeProps {
  status: TaskStatus | string;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  size = 'md',
  showIcon = true,
}) => {
  const normalized = status.toLowerCase();

  let bgClass = 'bg-slate-800 text-slate-300 border-slate-700';
  let dotClass = 'bg-slate-400';
  let Icon = Clock;
  let label = status.replace('_', ' ');

  switch (normalized) {
    case 'pending':
      bgClass = 'bg-amber-950/40 text-amber-300 border-amber-800/50';
      dotClass = 'bg-amber-400';
      Icon = Clock;
      label = 'Pending';
      break;
    case 'planning':
      bgClass = 'bg-indigo-950/50 text-indigo-300 border-indigo-700/50';
      dotClass = 'bg-indigo-400 animate-pulse';
      Icon = RotateCw;
      label = 'Planning';
      break;
    case 'awaiting_approval':
      bgClass = 'bg-purple-950/60 text-purple-200 border-purple-600/70 shadow-sm shadow-purple-500/20';
      dotClass = 'bg-purple-400 animate-ping';
      Icon = AlertTriangle;
      label = 'Awaiting Approval';
      break;
    case 'running':
      bgClass = 'bg-blue-950/50 text-blue-300 border-blue-600/50';
      dotClass = 'bg-blue-400 animate-pulse';
      Icon = Play;
      label = 'Running';
      break;
    case 'paused':
      bgClass = 'bg-yellow-950/40 text-yellow-300 border-yellow-700/50';
      dotClass = 'bg-yellow-400';
      Icon = Pause;
      label = 'Paused';
      break;
    case 'completed':
      bgClass = 'bg-emerald-950/50 text-emerald-300 border-emerald-600/50';
      dotClass = 'bg-emerald-400';
      Icon = CheckCircle2;
      label = 'Completed';
      break;
    case 'failed':
      bgClass = 'bg-rose-950/50 text-rose-300 border-rose-700/50';
      dotClass = 'bg-rose-400';
      Icon = XCircle;
      label = 'Failed';
      break;
    case 'cancelled':
      bgClass = 'bg-zinc-800 text-zinc-400 border-zinc-700';
      dotClass = 'bg-zinc-500';
      Icon = Ban;
      label = 'Cancelled';
      break;
  }

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
    lg: 'text-sm px-3.5 py-1.5 gap-2 font-medium',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border transition-all uppercase tracking-wider font-semibold ${bgClass} ${sizeClasses[size]}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${dotClass}`} />
      {showIcon && <Icon className="w-3.5 h-3.5" />}
      <span>{label}</span>
    </span>
  );
};
