import pytest
from app.services.risk_engine import calculate_risk, categorize

def test_categorize_thresholds():
    assert categorize(20.0) == "Low"
    assert categorize(45.0) == "Medium"
    assert categorize(65.0) == "High"
    assert categorize(85.0) == "Critical"

def test_calculate_risk_bounds():
    factors = {
        "shipping_disruption": 100.0,
        "geopolitical_tension": 100.0,
        "corridor_dependency": 100.0,
        "sanctions": 100.0,
        "conflict_intensity": 100.0
    }
    result = calculate_risk(factors, entity_type="corridor")
    assert 0.0 <= result["score"] <= 100.0
    assert result["category"] in ["Low", "Medium", "High", "Critical"]

def test_calculate_risk_low_factors():
    factors = {
        "shipping_disruption": 10.0,
        "geopolitical_tension": 10.0,
        "corridor_dependency": 10.0,
        "sanctions": 0.0,
        "conflict_intensity": 0.0,
        "supplier_dependency": 10.0,
        "historical_disruption": 0.0,
        "price_volatility": 0.0
    }
    result = calculate_risk(factors, entity_type="corridor")
    assert result["score"] < 30.0
    assert result["category"] == "Low"
