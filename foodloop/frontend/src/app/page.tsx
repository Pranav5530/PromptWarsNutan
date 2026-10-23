import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      {/* Hero */}
      <div className="text-center max-w-2xl mx-auto mb-12">
        <span className="inline-block px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold uppercase tracking-wider mb-4">
          Google Cloud & Vertex AI Hackathon
        </span>
        <h1 className="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight leading-tight">
          Rescue Surplus Food in <span className="text-emerald-600">&lt; 60 Seconds</span>
        </h1>
        <p className="mt-4 text-base text-slate-600 leading-relaxed">
          FoodLoop orchestrates multimodal Gemini intake, deterministic FSSAI safety gates, proximity matching, and volunteer dispatch to divert wholesome meals from landfills to verified shelters.
        </p>
      </div>

      {/* Role Portals */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Donor */}
        <Link
          href="/donor"
          className="group p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 hover:shadow-lg transition flex flex-col justify-between"
        >
          <div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition">
              🍲
            </div>
            <h2 className="text-lg font-bold text-slate-900 group-hover:text-emerald-700">Food Donor</h2>
            <p className="text-xs text-slate-500 mt-2">
              Snap a food photo or record a voice note. Gemini extracts portions, allergens, and holding window for 1-tap confirmation.
            </p>
          </div>
          <span className="text-xs font-bold text-emerald-600 mt-6 inline-flex items-center gap-1">
            Open Donor Portal →
          </span>
        </Link>

        {/* NGO Shelter */}
        <Link
          href="/ngo"
          className="group p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 hover:shadow-lg transition flex flex-col justify-between"
        >
          <div>
            <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition">
              🏠
            </div>
            <h2 className="text-lg font-bold text-slate-900 group-hover:text-blue-700">NGO Shelter</h2>
            <p className="text-xs text-slate-500 mt-2">
              Receive real-time match alerts scored by proximity, capacity, and dietary policy with plain-language explanations.
            </p>
          </div>
          <span className="text-xs font-bold text-blue-600 mt-6 inline-flex items-center gap-1">
            Open Shelter Portal →
          </span>
        </Link>

        {/* Volunteer */}
        <Link
          href="/volunteer"
          className="group p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 hover:shadow-lg transition flex flex-col justify-between"
        >
          <div>
            <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition">
              🛵
            </div>
            <h2 className="text-lg font-bold text-slate-900 group-hover:text-amber-700">Rescue Volunteer</h2>
            <p className="text-xs text-slate-500 mt-2">
              View active pickup tasks, unmasked contact numbers, Google Maps navigation routes, and 1-tap Proof of Delivery.
            </p>
          </div>
          <span className="text-xs font-bold text-amber-600 mt-6 inline-flex items-center gap-1">
            Open Volunteer App →
          </span>
        </Link>

        {/* Admin & Impact */}
        <Link
          href="/admin"
          className="group p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 hover:shadow-lg transition flex flex-col justify-between"
        >
          <div>
            <div className="w-12 h-12 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition">
              📊
            </div>
            <h2 className="text-lg font-bold text-slate-900 group-hover:text-purple-700">Impact Dashboard</h2>
            <p className="text-xs text-slate-500 mt-2">
              Auditable BigQuery analytics streaming kg rescued, meals served, CO₂ saved, and ML surplus hotspot predictions.
            </p>
          </div>
          <span className="text-xs font-bold text-purple-600 mt-6 inline-flex items-center gap-1">
            View Analytics →
          </span>
        </Link>
      </div>
    </div>
  );
}
