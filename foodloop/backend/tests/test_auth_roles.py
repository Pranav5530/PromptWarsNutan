import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_auth_unauthorized():
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401


def test_auth_donor_role():
    headers = {"Authorization": "Bearer test-donor:donor:user-donor-001"}
    res = client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["uid"] == "user-donor-001"
    assert data["role"] == "donor"


def test_auth_ngo_role():
    headers = {"Authorization": "Bearer test-ngo:ngo:user-ngo-101"}
    res = client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["uid"] == "user-ngo-101"
    assert data["role"] == "ngo"
