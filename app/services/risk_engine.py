from app.utils.scoring_utils import weighted_score

WEIGHTS_CORRIDOR = {
    "geopolitical_tension": 0.20,
    "sanctions": 0.10,
    "conflict_intensity": 0.15,
    "shipping_disruption": 0.20,
    "corridor_dependency": 0.15,
    "supplier_dependency": 0.10,
    "historical_disruption": 0.05,
    "price_volatility": 0.05,
}

WEIGHTS_SUPPLIER = {
    "geopolitical_tension": 0.25,
    "sanctions": 0.20,
    "conflict_intensity": 0.15,
    "shipping_disruption": 0.10,
    "corridor_dependency": 0.05,
    "supplier_dependency": 0.15,
    "historical_disruption": 0.05,
    "price_volatility": 0.05,
}

def categorize(score: float) -> str:
    if score <= 30.0:
        return "Low"
    elif score <= 55.0:
        return "Medium"
    elif score <= 75.0:
        return "High"
    return "Critical"

def calculate_risk(factors: dict, entity_type: str = "corridor") -> dict:
    """
    Pure deterministic risk scoring function.
    Returns: {"score": float, "category": str, "factors": dict}
    """
    weights = WEIGHTS_CORRIDOR if entity_type == "corridor" else WEIGHTS_SUPPLIER
    
    # Fill defaults for any missing factors
    complete_factors = {
        "geopolitical_tension": 50.0,
        "sanctions": 30.0,
        "conflict_intensity": 40.0,
        "shipping_disruption": 40.0,
        "corridor_dependency": 50.0,
        "supplier_dependency": 30.0,
        "historical_disruption": 40.0,
        "price_volatility": 30.0,
    }
    complete_factors.update(factors or {})

    score = weighted_score(complete_factors, weights)
    rounded_score = round(score, 1)

    return {
        "score": rounded_score,
        "category": categorize(rounded_score),
        "factors": complete_factors
    }
