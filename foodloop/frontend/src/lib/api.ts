const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function analyzeIntake(formData: FormData) {
  const res = await fetch(`${API_BASE}/agent/intake`, {
    method: 'POST',
    headers: {
      Authorization: 'Bearer test-donor:donor:user-donor-demo',
    },
    body: formData,
  });
  if (!res.ok) throw new Error('Intake extraction failed');
  return res.json();
}

export async function checkSafety(listingData: any) {
  const res = await fetch(`${API_BASE}/agent/safety-check`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer test-donor:donor:user-donor-demo',
    },
    body: JSON.stringify(listingData),
  });
  if (!res.ok) throw new Error('Safety evaluation failed');
  return res.json();
}

export async function getMatches(listingData: any) {
  const res = await fetch(`${API_BASE}/agent/match`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer test-donor:donor:user-donor-demo',
    },
    body: JSON.stringify(listingData),
  });
  if (!res.ok) throw new Error('Matching ranking failed');
  return res.json();
}

export async function dispatchVolunteer(dispatchData: any) {
  const res = await fetch(`${API_BASE}/agent/dispatch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer test-ngo:ngo:user-ngo-demo',
    },
    body: JSON.stringify(dispatchData),
  });
  if (!res.ok) throw new Error('Volunteer dispatch failed');
  return res.json();
}

export async function fetchImpactMetrics() {
  const res = await fetch(`${API_BASE}/analytics/impact`);
  if (!res.ok) throw new Error('Failed to fetch impact metrics');
  return res.json();
}

export async function fetchHotspots() {
  const res = await fetch(`${API_BASE}/analytics/forecast`);
  if (!res.ok) throw new Error('Failed to fetch hotspot forecast');
  return res.json();
}
