'use client';

import React, { useState } from 'react';
import { 
  AlertTriangle, 
  ShieldCheck, 
  X, 
  CheckCircle, 
  XCircle, 
  Hash, 
  Lock, 
  Clock 
} from 'lucide-react';
import { ApprovalRequest } from '@/types';
import { api } from '@/lib/api';

interface ApprovalModalProps {
  approval: ApprovalRequest;
  isOpen: boolean;
  onClose: () => void;
  onDecisionSubmitted: () => void;
}

export const ApprovalModal: React.FC<ApprovalModalProps> = ({
  approval,
  isOpen,
  onClose,
  onDecisionSubmitted,
}) => {
  const [decisionNotes, setDecisionNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleDecision = async (decision: 'approve' | 'reject') => {
    setIsSubmitting(true);
    setError(null);
    try {
      await api.decideApproval(approval.id, decision, decisionNotes);
      onDecisionSubmitted();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to submit decision.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-purple-500/40 rounded-2xl shadow-2xl shadow-purple-950/50 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 bg-gradient-to-r from-purple-950/60 via-slate-900 to-slate-900 border-b border-purple-500/20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400">
              <ShieldCheck className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs uppercase font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  Human Oversight Required
                </span>
                <span className="text-xs text-slate-400 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {new Date(approval.requested_at).toLocaleTimeString()}
                </span>
              </div>
              <h3 className="text-base font-semibold text-white mt-0.5">{approval.title}</h3>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5 max-h-[70vh] overflow-y-auto">
          {error && (
            <div className="p-3 bg-rose-950/50 border border-rose-600/50 rounded-xl text-rose-300 text-sm flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div>
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Description & Operational Context
            </label>
            <p className="text-sm text-slate-200 bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
              {approval.description}
            </p>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Exact Proposed Parameters (Integrity Bound)
            </label>
            <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono text-xs text-emerald-400 overflow-x-auto">
              <pre>{JSON.stringify(approval.parameters, null, 2)}</pre>
            </div>
          </div>

          <div>
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
              <Hash className="w-3.5 h-3.5 text-purple-400" />
              <span className="font-semibold uppercase tracking-wider">Cryptographic Signature & HMAC</span>
            </div>
            <div className="px-3 py-1.5 bg-slate-950/80 rounded-lg border border-slate-800/80 font-mono text-[11px] text-slate-400 break-all">
              {approval.payload_hash}
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Decision Justification / Auditor Notes (Optional)
            </label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Provide reason for approval or rejection (logged to audit ledger)..."
              rows={2}
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 focus:border-purple-500 rounded-xl text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-purple-500 transition-all"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-slate-950/60 border-t border-slate-800/80 flex items-center justify-between gap-3">
          <button
            onClick={onClose}
            disabled={isSubmitting}
            className="px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            Cancel
          </button>

          <div className="flex items-center gap-3">
            <button
              onClick={() => handleDecision('reject')}
              disabled={isSubmitting}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-700/50 text-sm font-semibold transition-all"
            >
              <XCircle className="w-4 h-4" />
              <span>Reject Request</span>
            </button>

            <button
              onClick={() => handleDecision('approve')}
              disabled={isSubmitting}
              className="inline-flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-sm font-semibold shadow-lg shadow-emerald-600/20 transition-all"
            >
              <CheckCircle className="w-4 h-4" />
              <span>{isSubmitting ? 'Verifying...' : 'Approve Execution'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
