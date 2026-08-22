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

def test_risk_corridor_endpoint(client):
    response = client.get("/api/risk?entity_type=corridor&entity_id=corr_hormuz")
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "factors" in data

def test_risk_supplier_endpoint(client):
    response = client.get("/api/risk?entity_type=supplier&entity_id=sup_saudi")
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "factors" in data

def test_scenarios_catalog_endpoint(client):
    response = client.get("/api/scenarios/catalog")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_scenarios_simulate_endpoint(client):
    payload = {
        "event_type": "hormuz_closure",
        "severity": 4,
        "duration_days": 30,
        "demand_delta_pct": 0.0,
        "affected_corridor_id": "corr_hormuz"
    }
    response = client.post("/api/scenarios/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "scenario_id" in data
    assert "supply_impact" in data

def test_routes_endpoint(client):
    response = client.get("/api/routes")
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert isinstance(data["routes"], list)

def test_reserves_optimize_endpoint(client):
    payload = {
        "scenario_id": "hormuz_closure_v1",
        "algorithm": "greedy",
        "include_planned": False
    }
    response = client.post("/api/reserves/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data

def test_reserves_sites_endpoint(client):
    response = client.get("/api/reserves/sites")
    assert response.status_code == 200
    data = response.json()
    assert "sites" in data
    assert isinstance(data["sites"], list)

def test_reserves_baseline_endpoint(client):
    response = client.get("/api/reserves/baseline")
    assert response.status_code == 200
    data = response.json()
    assert "baseline" in data

def test_reserves_scenarios_endpoint(client):
    response = client.get("/api/reserves/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data

def test_recommendations_endpoint(client):
    response = client.get("/api/recommendations/test_scenario_001")
    assert response.status_code == 200
    data = response.json()
    assert "actions" in data
    assert isinstance(data["actions"], list)

def test_explain_endpoint(client):
    payload = {"scenario_id": "test_scenario_001"}
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data

def test_events_endpoint(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_events_news_status_endpoint(client):
    response = client.get("/api/events/news/status")
    assert response.status_code == 200
    data = response.json()
    assert "events_processed_total" in data

def test_prices_latest_endpoint(client):
    response = client.get("/api/prices/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data

def test_prices_history_endpoint(client):
    response = client.get("/api/prices/history?timeframe=1M")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data

def test_admin_login_endpoint(client):
    # Test unauthorized login attempt
    response = client.post("/api/admin/login", json={"password": "wrong_password"})
    assert response.status_code == 401
