import pytest
from app.agents.logistics_agent import LogisticsAgent
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_logistics_agent_assignment():
    agent = LogisticsAgent()
    dispatch = await agent.assign_volunteer(
        listing_id="list-456",
        ngo_id="ngo-asha-001",
        donor_lat=12.9716,
        donor_lng=77.5946,
        ngo_lat=12.9750,
        ngo_lng=77.6000
    )
    assert dispatch.volunteer_id is not None
    assert dispatch.eta_minutes > 0
    assert "https://www.google.com/maps/dir/" in dispatch.directions_url
    assert dispatch.status == "assigned"


def test_proof_of_delivery_endpoint():
    headers = {"Authorization": "Bearer test-vol:volunteer:vol-rahul-01"}
    res = client.post(
        "/api/v1/agent/dispatch/disp-123/proof-of-delivery",
        data={"notes": "Delivered to Asha Shelter in person"},
        headers=headers
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "delivered"
    assert data["verified_by_volunteer"] == "vol-rahul-01"
