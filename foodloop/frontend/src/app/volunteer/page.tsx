'use client';

import React, { useState } from 'react';

export default function VolunteerPage() {
  const [step, setStep] = useState<'assigned' | 'picked_up' | 'delivered'>('assigned');
  const [photoUploaded, setPhotoUploaded] = useState(false);

  const task = {
    dispatch_id: 'disp-biryani-01',
    food_name: '25 kg Vegetable Biryani (~50 Meals)',
    donor: {
      name: 'Taj Gateway Restaurant',
      address: 'Residency Road, Bengaluru',
      phone: '+91-98765-43210'
    },
    destination: {
      name: 'Asha Shelter Home',
      address: 'Richmond Circle, Bengaluru',
      phone: '+91-98765-11001'
    },
    eta: '18 mins'
  };

  return (
    <div className="max-w-md mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">🛵 Volunteer Rescue Task</h1>
        <p className="text-xs text-slate-500">
          Rahul Sharma • Active on Two-Wheeler
        </p>
      </div>

      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        {/* Status Tracker */}
        <div className="flex justify-between items-center text-xs font-semibold mb-6">
          <span className={`px-2.5 py-1 rounded-full ${step === 'assigned' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-400'}`}>
            1. Pickup
          </span>
          <span className="text-slate-300">→</span>
          <span className={`px-2.5 py-1 rounded-full ${step === 'picked_up' ? 'bg-blue-100 text-blue-800' : 'bg-slate-100 text-slate-400'}`}>
            2. Transit
          </span>
          <span className="text-slate-300">→</span>
          <span className={`px-2.5 py-1 rounded-full ${step === 'delivered' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-400'}`}>
            3. Delivered
          </span>
        </div>

        <h2 className="text-lg font-bold text-slate-900 mb-1">{task.food_name}</h2>
        <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
          Perishable • ETA: {task.eta}
        </span>

        {/* Route Details */}
        <div className="my-6 space-y-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-slate-400 font-semibold uppercase">Step 1: Pickup Location</span>
            <p className="text-sm font-bold text-slate-800 mt-0.5">{task.donor.name}</p>
            <p className="text-slate-500">{task.donor.address}</p>
            <p className="text-slate-600 font-mono mt-1">📞 {task.donor.phone}</p>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-slate-400 font-semibold uppercase">Step 2: Dropoff Shelter</span>
            <p className="text-sm font-bold text-slate-800 mt-0.5">{task.destination.name}</p>
            <p className="text-slate-500">{task.destination.address}</p>
            <p className="text-slate-600 font-mono mt-1">📞 {task.destination.phone}</p>
          </div>
        </div>

        {/* Actions based on step */}
        {step === 'assigned' && (
          <button
            onClick={() => setStep('picked_up')}
            className="w-full py-3 bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm rounded-xl transition"
          >
            Confirm Food Picked Up 📦
          </button>
        )}

        {step === 'picked_up' && (
          <div className="space-y-3">
            <div className="p-4 border-2 border-dashed border-slate-300 rounded-xl text-center">
              <span className="text-2xl mb-1 block">📸</span>
              <p className="text-xs font-bold text-slate-700">Upload Proof of Delivery (PoD)</p>
              <p className="text-[10px] text-slate-400">Photo with shelter coordinator at handover</p>
              <input
                type="file"
                accept="image/*"
                onChange={() => setPhotoUploaded(true)}
                className="mt-2 text-xs text-slate-500"
              />
            </div>

            <button
              onClick={() => setStep('delivered')}
              disabled={!photoUploaded}
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl transition"
            >
              Complete Rescue & Submit Proof ✓
            </button>
          </div>
        )}

        {step === 'delivered' && (
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-center">
            <div className="w-10 h-10 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-xl mx-auto mb-2">
              ✓
            </div>
            <h3 className="font-bold text-emerald-900 text-sm">Rescue Completed!</h3>
            <p className="text-xs text-emerald-700 mt-1">
              50 meals safely delivered to Asha Shelter Home. Event streamed to BigQuery impact metrics!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
