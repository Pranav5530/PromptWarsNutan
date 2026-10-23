from fastapi import APIRouter, Depends
from typing import List
from app.schemas.foodloop import ImpactMetrics, SurplusHotspot
from app.services.bigquery import bigquery_service

router = APIRouter(prefix="/analytics", tags=["Impact Analytics & BigQuery"])


@router.get("/impact", response_model=ImpactMetrics)
async def get_live_impact_metrics():
    """
    Returns real-time aggregated rescue metrics (kg rescued, meals served, CO2 offset, average match time).
    """
    return await bigquery_service.get_aggregated_impact_metrics()


@router.get("/forecast", response_model=List[SurplusHotspot])
async def get_surplus_hotspot_forecast():
    """
    Returns BigQuery ML predictions for surplus food hotspots by area and time of day.
    """
    return await bigquery_service.get_surplus_hotspots()
