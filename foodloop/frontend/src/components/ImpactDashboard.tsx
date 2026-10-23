import React from 'react';

export interface ImpactMetricsProps {
  totalKgRescued: number;
  totalMealsServed: number;
  co2SavedKg: number;
  avgMatchTimeSec: number;
  activeRescues: number;
}

export interface SurplusHotspotProps {
  areaName: string;
  city: string;
  peakHour: string;
  predictedSurplusKg: number;
  activeDonorCount: number;
}

export const ImpactDashboard: React.FC<{
  metrics: ImpactMetricsProps;
  hotspots: SurplusHotspotProps[];
}> = ({ metrics, hotspots }) => {
  return (
    <div className="p-6 bg-slate-50 min-h-screen text-slate-800">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-emerald-800 flex items-center gap-2">
            🌱 FoodLoop Impact & Forecasting
          </h1>
          <p className="text-sm text-slate-500">
            Real-time rescue tracking streamed to Google BigQuery & ML Forecasting
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-semibold uppercase">
            BigQuery Live Pipeline
          </span>
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold uppercase">
            Vertex AI Orchestrated
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Total Rescued
          </span>
          <div className="mt-2 text-3xl font-extrabold text-slate-900">
            {metrics.totalKgRescued.toLocaleString()}{' '}
            <span className="text-sm font-medium text-slate-500">kg</span>
          </div>
          <p className="text-xs text-emerald-600 mt-1 font-medium">↑ 100% diverted from landfill</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Nutritious Meals Served
          </span>
          <div className="mt-2 text-3xl font-extrabold text-emerald-600">
            {metrics.totalMealsServed.toLocaleString()}
          </div>
          <p className="text-xs text-slate-400 mt-1">Calibrated at 0.5 kg / meal</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            CO₂ Offset
          </span>
          <div className="mt-2 text-3xl font-extrabold text-blue-600">
            {metrics.co2SavedKg.toLocaleString()}{' '}
            <span className="text-sm font-medium text-slate-500">kg CO₂e</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">2.5 kg CO₂e saved per kg food</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Average Match Time
          </span>
          <div className="mt-2 text-3xl font-extrabold text-amber-600">
            {metrics.avgMatchTimeSec}{' '}
            <span className="text-sm font-medium text-slate-500">sec</span>
          </div>
          <p className="text-xs text-emerald-600 mt-1 font-medium">SLA &lt; 60s guaranteed</p>
        </div>
      </div>

      {/* Surplus Hotspot Forecast (BigQuery ML) */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              📍 Predicted Surplus Hotspots (BigQuery ML)
            </h2>
            <p className="text-xs text-slate-500">
              Anticipate surplus generation to preposition volunteers before shift changes
            </p>
          </div>
        </div>

        <div className="divide-y divide-slate-100">
          {hotspots.map((h, i) => (
            <div key={i} className="py-4 flex justify-between items-center">
              <div>
                <h3 className="font-semibold text-slate-800">{h.areaName}</h3>
                <p className="text-xs text-slate-500">
                  {h.city} • {h.activeDonorCount} registered donors
                </p>
              </div>
              <div className="text-right">
                <span className="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                  Peak: {h.peakHour}
                </span>
                <p className="text-sm font-bold text-slate-900 mt-1">
                  ~{h.predictedSurplusKg} kg expected
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
