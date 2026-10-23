import pytest
from app.services.bigquery import bigquery_service
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_bigquery_streaming_and_kpis():
    # Stream a newly delivered rescue event
    await bigquery_service.stream_event({
        "event_id": "test-rescue-evt",
        "listing_id": "list-999",
        "event_type": "delivered",
        "kg_rescued": 50.0,
        "meals_served": 100,
        "match_latency_sec": 12.0
    })

    metrics = await bigquery_service.get_aggregated_impact_metrics()
    assert metrics.total_kg_rescued >= 125.0 # Includes seed events (75kg) + 50kg
    assert metrics.total_meals_served >= 250
    assert metrics.co2_saved_kg >= 312.5
    assert metrics.avg_match_time_sec < 60.0


def test_analytics_api_endpoints():
    res_impact = client.get("/api/v1/analytics/impact")
    assert res_impact.status_code == 200
    data_impact = res_impact.json()
    assert "total_kg_rescued" in data_impact
    assert "total_meals_served" in data_impact

    res_forecast = client.get("/api/v1/analytics/forecast")
    assert res_forecast.status_code == 200
    data_forecast = res_forecast.json()
    assert isinstance(data_forecast, list)
    assert len(data_forecast) >= 3
    assert data_forecast[0]["city"] == "Bengaluru"
