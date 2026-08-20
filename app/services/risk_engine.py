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

def calculate_ml_risk(features_dict: dict) -> dict:
    """
    Attempts to calculate risk using the XGBoost ML model if available.
    Returns: {"ml_score": float, "shap_top3": [{"feature": str, "contribution": float}]}
    or None if model is not loaded/available.
    """
    try:
        import xgboost as xgb
        import pandas as pd
        import joblib
        import json
        from pathlib import Path
        
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        MODELS_DIR = BASE_DIR / "ml" / "models"
        
        model_path = MODELS_DIR / "xgboost_risk_model.json"
        features_path = MODELS_DIR / "risk_features.json"
        explainer_path = MODELS_DIR / "shap_explainer.joblib"
        
        if not (model_path.exists() and features_path.exists()):
            return None
            
        with open(features_path, "r") as f:
            feature_cols = json.load(f)
            
        # Build dataframe using defaults for missing features
        row = {col: features_dict.get(col, 0.0) for col in feature_cols}
        df = pd.DataFrame([row])
        
        # Load model and predict
        model = xgb.XGBRegressor()
        model.load_model(model_path)
        ml_score = float(model.predict(df)[0])
        ml_score = max(0.0, min(100.0, ml_score))
        
        # SHAP explainability
        shap_top3 = []
        if explainer_path.exists():
            explainer = joblib.load(explainer_path)
            shap_values = explainer.shap_values(df)
            
            # Get top 3 indices by absolute magnitude
            import numpy as np
            top3_idx = np.argsort(np.abs(shap_values[0]))[-3:][::-1]
            
            for idx in top3_idx:
                shap_top3.append({
                    "feature": feature_cols[idx],
                    "contribution": float(shap_values[0][idx])
                })
                
        return {
            "ml_score": round(ml_score, 1),
            "shap_top3": shap_top3
        }
    except Exception as e:
        print(f"Failed to calculate ML risk: {e}")
        return None
