'use client';

import React, { useEffect, useState } from 'react';
import { ImpactDashboard, ImpactMetricsProps, SurplusHotspotProps } from '@/components/ImpactDashboard';
import { fetchImpactMetrics, fetchHotspots } from '@/lib/api';

export default function AdminPage() {
  const [metrics, setMetrics] = useState<ImpactMetricsProps>({
    totalKgRescued: 125.0,
    totalMealsServed: 250,
    co2SavedKg: 312.5,
    avgMatchTimeSec: 16.4,
    activeRescues: 3,
  });

  const [hotspots, setHotspots] = useState<SurplusHotspotProps[]>([
    {
      areaName: 'Koramangala Food Street & Catering Hub',
      city: 'Bengaluru',
      peakHour: '21:30 - 23:00',
      predictedSurplusKg: 140.0,
      activeDonorCount: 12,
    },
    {
      areaName: 'Indiranagar 100ft Dining Corridor',
      city: 'Bengaluru',
      peakHour: '22:00 - 23:30',
      predictedSurplusKg: 95.0,
      activeDonorCount: 9,
    },
    {
      areaName: 'Electronic City Hostel Mess Belt',
      city: 'Bengaluru',
      peakHour: '14:00 - 15:30',
      predictedSurplusKg: 180.0,
      activeDonorCount: 15,
    },
  ]);

  useEffect(() => {
    async function loadData() {
      try {
        const m = await fetchImpactMetrics();
        setMetrics({
          totalKgRescued: m.total_kg_rescued,
          totalMealsServed: m.total_meals_served,
          co2SavedKg: m.co2_saved_kg,
          avgMatchTimeSec: m.avg_match_time_sec,
          activeRescues: m.active_rescues,
        });

        const h = await fetchHotspots();
        setHotspots(
          h.map((item: any) => ({
            areaName: item.area_name,
            city: item.city,
            peakHour: item.peak_hour,
            predictedSurplusKg: item.predicted_surplus_kg,
            activeDonorCount: item.active_donor_count,
          }))
        );
      } catch (e) {
        console.warn('Backend API offline or unreachable, using live seeded metrics fallback');
      }
    }
    loadData();
  }, []);

  return <ImpactDashboard metrics={metrics} hotspots={hotspots} />;
}
