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

def calculate_ml_risk(features_dict: dict, db=None, entity_id=None) -> dict:
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

async def calculate_ml_risk_async(features_dict: dict, db=None, entity_id=None, entity_type="corridor") -> dict:
    if db is None or entity_id is None:
        print(f"Falling back to deterministic factors for ML features for {entity_type} {entity_id}")
        return calculate_ml_risk(features_dict)
        
    print(f"Building full feature vector from DB for {entity_type} {entity_id}")
    
    ml_features = {
        "political_stability": 0.0,
        "rule_of_law": 0.0,
        "control_of_corruption": 0.0,
        "government_effectiveness": 0.0,
        "sanction_entity_count": 0,
        "sanctions_severity": 0.0,
        "oil_production_tbpd": 0.0,
        "oil_exports_tbpd": 0.0,
        "import_share_pct_qty": 0.0,
        "hhi_qty": 0.0,
        "conflict_intensity": 0.0,
        "conflict_event_count": 0,
        "avg_media_tone": 0.0
    }
    
    # Supplier related
    all_suppliers = await db.suppliers.find({}).to_list(length=100)
    total_export = sum([s.get("current_export_bpd", 0) for s in all_suppliers])
    if total_export > 0:
        ml_features["hhi_qty"] = sum([(s.get("current_export_bpd", 0) / total_export * 100)**2 for s in all_suppliers])
    
    if entity_type == "supplier":
        supplier = next((s for s in all_suppliers if s["_id"] == entity_id), None)
        if supplier:
            wgi = supplier.get("wgi_indicators", {})
            ml_features["political_stability"] = wgi.get("political_stability", 0.0)
            ml_features["rule_of_law"] = wgi.get("rule_of_law", 0.0)
            ml_features["control_of_corruption"] = wgi.get("control_of_corruption", 0.0)
            ml_features["government_effectiveness"] = wgi.get("government_effectiveness", 0.0)
            
            ml_features["oil_production_tbpd"] = supplier.get("max_capacity_bpd", 0) / 1000.0
            ml_features["oil_exports_tbpd"] = supplier.get("current_export_bpd", 0) / 1000.0
            
            if total_export > 0:
                ml_features["import_share_pct_qty"] = (supplier.get("current_export_bpd", 0) / total_export) * 100.0
                
    elif entity_type == "corridor":
        corridor = await db.corridors.find_one({"_id": entity_id})
        if corridor:
            ml_features["import_share_pct_qty"] = corridor.get("share_of_india_imports_pct", 0.0)
            
        routes = await db.routes.find({"corridor_id": entity_id}).to_list(length=100)
        supplier_ids = list(set([r["from_node"] for r in routes]))
        sups = [s for s in all_suppliers if s["_id"] in supplier_ids]
        
        if sups:
            wgis = [s.get("wgi_indicators", {}) for s in sups if "wgi_indicators" in s]
            if wgis:
                ml_features["political_stability"] = sum([w.get("political_stability", 0.0) for w in wgis]) / len(wgis)
                ml_features["rule_of_law"] = sum([w.get("rule_of_law", 0.0) for w in wgis]) / len(wgis)
                ml_features["control_of_corruption"] = sum([w.get("control_of_corruption", 0.0) for w in wgis]) / len(wgis)
                ml_features["government_effectiveness"] = sum([w.get("government_effectiveness", 0.0) for w in wgis]) / len(wgis)
                
            ml_features["oil_production_tbpd"] = sum([s.get("max_capacity_bpd", 0) for s in sups]) / 1000.0
            ml_features["oil_exports_tbpd"] = sum([s.get("current_export_bpd", 0) for s in sups]) / 1000.0

    # Risk Events
    events = await db.risk_events.find({}).to_list(length=100)
    entity_events = []
    for e in events:
        if entity_type == "corridor" and e.get("corridor_id") == entity_id:
            entity_events.append(e)
        elif entity_type == "supplier":
            sup = next((s for s in all_suppliers if s["_id"] == entity_id), None)
            if sup and sup["name"] in e.get("title", ""):
                entity_events.append(e)

    sanc_events = [e for e in entity_events if e.get("category") == "sanctions"]
    ml_features["sanction_entity_count"] = len(sanc_events)
    if sanc_events:
        ml_features["sanctions_severity"] = sum([e.get("severity", 0) for e in sanc_events]) / len(sanc_events)
        
    conf_events = [e for e in entity_events if e.get("category") in ["conflict", "shipping_attack", "diplomatic"]]
    ml_features["conflict_event_count"] = len(conf_events)
    if conf_events:
        ml_features["conflict_intensity"] = sum([e.get("severity", 0) for e in conf_events]) / len(conf_events)
        
    return calculate_ml_risk(ml_features)
