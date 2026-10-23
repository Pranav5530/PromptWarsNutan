'use client';

import React, { useState } from 'react';
import { analyzeIntake, checkSafety, getMatches } from '@/lib/api';

export default function DonorPage() {
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [draft, setDraft] = useState<any>(null);
  const [safety, setSafety] = useState<any>(null);
  const [matches, setMatches] = useState<any>(null);
  const [confirmed, setConfirmed] = useState(false);

  // Quick preset meals for testing
  const presets = [
    '25 kg Vegetable Biryani freshly prepared in catering vessel, lunch leftovers',
    '15 kg Yellow Dal & 50 Rotis from hostel dinner mess',
    '30 kg Chicken Curry with Steamed Rice from banquet hall',
    '10 kg Assorted Bakery Bread & Buns from morning bake'
  ];

  const handleAnalyze = async (sampleText?: string) => {
    const textToAnalyze = sampleText || notes;
    if (!textToAnalyze) return;

    setLoading(true);
    setConfirmed(false);
    setMatches(null);

    try {
      const formData = new FormData();
      formData.append('donor_notes', textToAnalyze);

      // Step 1: Intake Agent (Gemini 2.5 Flash)
      const intakeRes = await analyzeIntake(formData);
      setDraft(intakeRes);

      // Step 2: Safety Rules Engine (Deterministic FSSAI + Reasoning)
      const safetyRes = await checkSafety({
        donor_id: 'donor-taj-01',
        donor_name: 'Taj Gateway Restaurant',
        food_name: intakeRes.food_name,
        category: intakeRes.category,
        estimated_kg: intakeRes.estimated_kg,
        meal_count: intakeRes.meal_count,
        dietary_type: intakeRes.dietary_type,
        allergens: intakeRes.allergens,
        prep_timestamp: new Date().toISOString(),
        storage_condition: 'room_temp',
        ambient_temp_celsius: 27.0,
        donor_latitude: 12.9716,
        donor_longitude: 77.5946,
        donor_address_masked: 'Residency Road, Bengaluru'
      });
      setSafety(safetyRes);
    } catch (err: any) {
      alert('Error processing food listing: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmListing = async () => {
    if (!draft || !safety) return;
    setLoading(true);

    try {
      // Step 3: Trigger Matching Agent
      const matchRes = await getMatches({
        donor_id: 'donor-taj-01',
        donor_name: 'Taj Gateway Restaurant',
        food_name: draft.food_name,
        category: draft.category,
        estimated_kg: draft.estimated_kg,
        meal_count: draft.meal_count,
        dietary_type: draft.dietary_type,
        allergens: draft.allergens,
        prep_timestamp: new Date().toISOString(),
        storage_condition: 'room_temp',
        ambient_temp_celsius: 27.0,
        donor_latitude: 12.9716,
        donor_longitude: 77.5946,
        donor_address_masked: 'Residency Road, Bengaluru'
      });
      setMatches(matchRes);
      setConfirmed(true);
    } catch (err: any) {
      alert('Error triggering matching agent: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">🍲 Donor Food Intake</h1>
        <p className="text-sm text-slate-500">
          Upload photo or voice description. Gemini extracts metadata for one-tap confirmation.
        </p>
      </div>

      {/* Input Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm mb-6">
        <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">
          Surplus Description / Voice Transcription
        </label>
        <textarea
          rows={3}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="E.g. We have 25 kg vegetable biryani prepared 45 mins ago..."
          className="w-full p-3 text-sm rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none"
        />

        {/* Quick Demo Samples */}
        <div className="mt-3">
          <span className="text-xs text-slate-400 font-medium">Quick Demo Samples:</span>
          <div className="flex flex-wrap gap-2 mt-1.5">
            {presets.map((p, i) => (
              <button
                key={i}
                type="button"
                onClick={() => {
                  setNotes(p);
                  handleAnalyze(p);
                }}
                className="text-xs px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-600 rounded-lg transition"
              >
                {p.split(' ')[2] || 'Sample'}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={() => handleAnalyze()}
          disabled={loading || !notes}
          className="mt-4 w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl transition"
        >
          {loading ? 'Analyzing with Gemini 2.5 Flash...' : 'Extract & Check Safety'}
        </button>
      </div>

      {/* Extracted Metadata Card */}
      {draft && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Extracted Listing</span>
              <h2 className="text-xl font-bold text-slate-900">{draft.food_name}</h2>
            </div>
            {safety && (
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                  safety.verdict === 'Safe'
                    ? 'bg-emerald-100 text-emerald-800'
                    : safety.verdict === 'Risky'
                    ? 'bg-amber-100 text-amber-800'
                    : 'bg-rose-100 text-rose-800'
                }`}
              >
                {safety.verdict === 'Safe' ? '✓ ' : '⚠️ '}
                FSSAI {safety.verdict}
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs mb-4">
            <div className="p-3 bg-slate-50 rounded-xl">
              <span className="text-slate-400 font-medium">Estimated Qty</span>
              <p className="text-sm font-bold text-slate-800 mt-0.5">{draft.estimated_kg} kg</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl">
              <span className="text-slate-400 font-medium">Meal Portions</span>
              <p className="text-sm font-bold text-slate-800 mt-0.5">~{draft.meal_count} meals</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl">
              <span className="text-slate-400 font-medium">Dietary Type</span>
              <p className="text-sm font-bold text-slate-800 mt-0.5 capitalize">{draft.dietary_type}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl">
              <span className="text-slate-400 font-medium">Safe Window</span>
              <p className="text-sm font-bold text-slate-800 mt-0.5">{draft.safe_consume_hours} Hours</p>
            </div>
          </div>

          {safety && (
            <div className="p-3 bg-slate-50 border border-slate-100 rounded-xl text-xs text-slate-600 mb-4">
              <span className="font-bold text-slate-800">Safety Agent Audit: </span>
              {safety.ai_explanation}
            </div>
          )}

          {!confirmed && safety?.verdict !== 'Rejected' && (
            <button
              onClick={handleConfirmListing}
              disabled={loading}
              className="w-full py-3 bg-slate-900 hover:bg-emerald-600 text-white font-bold text-sm rounded-xl transition"
            >
              {loading ? 'Matching with Nearby Shelters...' : '1-Tap Confirm Listing →'}
            </button>
          )}

          {confirmed && matches && (
            <div className="mt-4 p-4 bg-emerald-50 border border-emerald-200 rounded-xl">
              <h3 className="font-bold text-emerald-800 text-sm flex items-center gap-2">
                ✓ Matched with {matches.selected_ngo?.ngo_name}!
              </h3>
              <p className="text-xs text-emerald-700 mt-1">
                Matched in {matches.match_latency_sec}s • {matches.selected_ngo?.reasoning}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
