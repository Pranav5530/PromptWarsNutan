import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'FoodLoop | Autonomous Surplus Food Rescue',
  description: 'AI-Powered Multi-Agent Surplus Food Rescue Platform powered by Google Vertex AI & Firebase.',
  manifest: '/manifest.json',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
        {/* Top Navbar */}
        <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2 font-black text-xl text-emerald-700">
              <span className="text-2xl">🌱</span>
              <span>FoodLoop</span>
            </Link>

            <nav className="flex items-center gap-1 sm:gap-4 text-sm font-medium">
              <Link href="/donor" className="px-3 py-1.5 rounded-lg text-slate-600 hover:text-emerald-700 hover:bg-emerald-50">
                Donor
              </Link>
              <Link href="/ngo" className="px-3 py-1.5 rounded-lg text-slate-600 hover:text-emerald-700 hover:bg-emerald-50">
                NGO Shelter
              </Link>
              <Link href="/volunteer" className="px-3 py-1.5 rounded-lg text-slate-600 hover:text-emerald-700 hover:bg-emerald-50">
                Volunteer
              </Link>
              <Link href="/admin" className="px-3 py-1.5 rounded-lg text-slate-600 hover:text-emerald-700 hover:bg-emerald-50">
                Impact Dashboard
              </Link>
            </nav>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1">
          {children}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
          <p>© 2026 FoodLoop. Powered by Google Cloud (Vertex AI Gemini 2.5 Flash, Firebase & BigQuery ML).</p>
        </footer>
      </body>
    </html>
  );
}
