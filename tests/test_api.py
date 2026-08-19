import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_dashboard_endpoint(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "overall_risk" in data
    assert "corridor_risks" in data
    assert "top_corridors" in data

def test_suppliers_endpoint(client):
    response = client.get("/api/suppliers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_network_endpoint(client):
    response = client.get("/api/network")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data

def test_risk_endpoint(client):
    response = client.get("/api/risk?entity_type=corridor&entity_id=corr_hormuz")
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "factors" in data

def test_scenarios_catalog_endpoint(client):
    response = client.get("/api/scenarios/catalog")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_events_endpoint(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
