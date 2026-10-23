'use client';

import React, { useState } from 'react';
import { dispatchVolunteer } from '@/lib/api';

export default function NgoPage() {
  const [accepted, setAccepted] = useState(false);
  const [dispatch, setDispatch] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Incoming active match alert for Asha Shelter Home
  const incomingMatch = {
    listing_id: 'list-biryani-25kg',
    food_name: 'Hyderabadi Vegetable Biryani',
    donor_name: 'Taj Gateway Restaurant',
    donor_area: 'Residency Road (1.8 km away)',
    estimated_kg: 25,
    meal_count: 50,
    dietary: 'Vegetarian',
    urgency_window: '3.5 Hours remaining',
    reasoning: 'Ranked #1: Located 1.8 km away, matching your 60-meal capacity deficit, fully compatible vegetarian policy.'
  };

  const handleAccept = async () => {
    setLoading(true);
    try {
      const res = await dispatchVolunteer({
        listing_id: incomingMatch.listing_id,
        ngo_id: 'ngo-asha-001',
        donor_lat: 12.9716,
        donor_lng: 77.5946,
        ngo_lat: 12.9750,
        ngo_lng: 77.6000,
      });
      setDispatch(res);
      setAccepted(true);
    } catch (err: any) {
      alert('Dispatch failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">🏠 NGO Shelter Dispatch Portal</h1>
        <p className="text-sm text-slate-500">
          Asha Shelter Home (Active • Capacity: 60 Meals • Pure Veg)
        </p>
      </div>

      {!accepted ? (
        <div className="bg-white p-6 rounded-2xl border-2 border-emerald-500 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold uppercase animate-pulse">
              🔔 New Match Alert
            </span>
            <span className="text-xs text-slate-400 font-semibold">Listing-to-Match: 18s</span>
          </div>

          <h2 className="text-xl font-black text-slate-900">{incomingMatch.food_name}</h2>
          <p className="text-xs text-slate-500 mt-1">From: {incomingMatch.donor_name} • {incomingMatch.donor_area}</p>

          <div className="grid grid-cols-3 gap-3 my-4 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl text-center">
              <span className="text-slate-400 font-medium">Quantity</span>
              <p className="text-sm font-bold text-slate-800 mt-0.5">{incomingMatch.estimated_kg} kg</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl text-center">
              <span className="text-slate-400 font-medium">Portions</span>
              <p className="text-sm font-bold text-emerald-600 mt-0.5">~{incomingMatch.meal_count} meals</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl text-center">
              <span className="text-slate-400 font-medium">Safe Window</span>
              <p className="text-sm font-bold text-slate-800 mt-0.5">{incomingMatch.urgency_window}</p>
            </div>
          </div>

          <div className="p-3.5 bg-blue-50 border border-blue-100 rounded-xl text-xs text-blue-900 mb-6">
            <span className="font-bold">Matching Agent Rationale: </span>
            {incomingMatch.reasoning}
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleAccept}
              disabled={loading}
              className="flex-1 py-3 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl transition shadow"
            >
              {loading ? 'Assigning Nearest Volunteer...' : 'Accept Surplus Match ✓'}
            </button>
            <button
              onClick={() => alert('Declined: Listing will automatically cascade to candidate #2.')}
              className="px-4 py-3 bg-slate-100 hover:bg-slate-200 text-slate-600 font-semibold text-sm rounded-xl transition"
            >
              Decline
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm text-center">
          <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
            ✓
          </div>
          <h2 className="text-xl font-bold text-slate-900">Match Accepted & Volunteer Assigned!</h2>
          <p className="text-xs text-slate-500 mt-1">
            Logistics Agent dispatched the nearest volunteer to collect and transport the food.
          </p>

          {dispatch && (
            <div className="my-6 p-4 bg-slate-50 rounded-xl border border-slate-200 text-left text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-500">Assigned Volunteer:</span>
                <span className="font-bold text-slate-900">{dispatch.volunteer_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Contact:</span>
                <span className="font-bold text-slate-900">{dispatch.volunteer_phone}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Estimated Delivery Time (ETA):</span>
                <span className="font-bold text-emerald-600">~{dispatch.eta_minutes} Minutes</span>
              </div>
            </div>
          )}

          <a
            href={dispatch?.directions_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block py-2.5 px-6 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition"
          >
            Track Route on Google Maps 🗺️
          </a>
        </div>
      )}
    </div>
  );
}
