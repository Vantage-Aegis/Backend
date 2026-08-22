import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.services.oil_price_service import OilPriceService

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_get_latest_price(client):
    response = client.get("/api/prices/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    price_info = data["data"]
    assert "price" in price_info
    assert price_info["price"] > 0
    assert price_info["currency"] == "USD"
    assert "code" in price_info
    assert price_info["code"] == "BRENT_CRUDE_USD"

def test_get_price_history(client):
    # Test default 1M timeframe (30 days)
    response = client.get("/api/prices/history")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 30

    # Test 1W timeframe
    response_1w = client.get("/api/prices/history?timeframe=1W")
    assert response_1w.status_code == 200
    assert len(response_1w.json()["data"]) == 7

    # Test 1Y timeframe
    response_1y = client.get("/api/prices/history?timeframe=1Y")
    assert response_1y.status_code == 200
    assert len(response_1y.json()["data"]) == 12

    # Test MAX timeframe
    response_max = client.get("/api/prices/history?timeframe=MAX")
    assert response_max.status_code == 200
    assert len(response_max.json()["data"]) > 50

    point = data["data"][0]
    assert "date" in point
    assert "price" in point
    assert "anomaly_flag" in point

def test_sync_price_endpoint(client):
    response = client.post("/api/prices/sync")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["price"] > 0

def test_dashboard_contains_live_brent_price(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "live_brent_price" in data
    if data["live_brent_price"]:
        assert "price" in data["live_brent_price"]
        assert data["live_brent_price"]["price"] > 0
        assert data["live_brent_price"]["currency"] == "USD"

@pytest.mark.asyncio
async def test_oil_price_service_live_fetch():
    live_data = await OilPriceService.fetch_live_brent_price()
    if live_data:
        assert "price" in live_data
        assert live_data["price"] > 0
        assert live_data["currency"] == "USD"
        assert live_data["code"] == "BRENT_CRUDE_USD"
