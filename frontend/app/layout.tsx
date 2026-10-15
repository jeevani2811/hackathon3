import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';

export const metadata: Metadata = {
  title: 'OmniAgent | Autonomous Strategic Market Operations & Multi-Agent Intelligence',
  description: 'Enterprise-grade agentic AI application that autonomously plans, reasons, models financial TCO, and coordinates specialized agents with human-in-the-loop controls.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-[#0b0f19] text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
        <Navbar />
        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="w-full border-t border-slate-800/80 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
            <p>&copy; 2026 OmniAgent Intelligent Systems. Production-Ready Multi-Agent Architecture.</p>
            <div className="flex items-center gap-4 text-slate-400">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                SSE Streaming Active
              </span>
              <span>|</span>
              <span>FastAPI &amp; Next.js App Router</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
