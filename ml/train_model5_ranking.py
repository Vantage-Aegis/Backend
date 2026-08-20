import os
import pandas as pd
import xgboost as xgb
import joblib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "ml" / "models"
os.makedirs(MODELS_DIR, exist_ok=True)

def train_supplier_ranking():
    print("Loading data for Supplier Ranking (Model 5)...")
    suppliers = pd.read_csv(DATA_DIR / "supplier_import_records.csv")
    wgi = pd.read_csv(DATA_DIR / "wgi_scores_by_country_year.csv")
    imports = pd.read_csv(DATA_DIR / "india_import_share_by_country.csv")
    
    # Feature Engineering
    wgi["route_risk_score"] = 100 - wgi[["political_stability", "rule_of_law"]].mean(axis=1)
    
    total_years = suppliers["start_year"].nunique()
    reliability = suppliers.groupby("country_code")["start_year"].nunique().reset_index()
    reliability.columns = ["country_code", "years_present"]
    reliability["supplier_reliability"] = reliability["years_present"] / total_years
    
    features = suppliers.merge(wgi[["country_code", "year", "route_risk_score"]],
                               left_on=["country_code", "start_year"],
                               right_on=["country_code", "year"], how="left")
    
    features = features.merge(reliability[["country_code", "supplier_reliability"]],
                              on="country_code", how="left")
                              
    features = features.merge(imports[["country_code", "start_year", "import_share_pct_qty"]],
                              on=["country_code", "start_year"], how="left")
    
    # Cost competitiveness (1 / (unit_cost / median_unit_cost_that_year))
    median_costs = features.groupby("start_year")["unit_cost_usd_per_t"].median().reset_index()
    median_costs.columns = ["start_year", "median_cost"]
    features = features.merge(median_costs, on="start_year", how="left")
    features["cost_competitiveness"] = 1.0 / (features["unit_cost_usd_per_t"] / features["median_cost"])
    
    # Fill NAs and Infs
    import numpy as np
    features.replace([np.inf, -np.inf], np.nan, inplace=True)
    numeric_cols = features.select_dtypes(include=['float64', 'int64']).columns
    features[numeric_cols] = features[numeric_cols].fillna(features[numeric_cols].median())

    # Labels - XGBoost NDCG handles relevance labels up to 31 by default, or disable exp gain
    max_rank = features.groupby("start_year")["rank_by_volume"].transform("max")
    features["relevance_label"] = np.clip((max_rank - features["rank_by_volume"] + 1).fillna(0), 0, 31).astype(int)
    
    # Ensure sorted by group
    features = features.sort_values(by=["start_year", "country_code"])
    
    feature_cols = [
        "volume_000t", "value_million_usd", "unit_cost_usd_per_t",
        "route_risk_score", "supplier_reliability", "import_share_pct_qty",
        "cost_competitiveness"
    ]
    
    X = features[feature_cols]
    y = features["relevance_label"]
    group_sizes = features.groupby("start_year").size().values
    
    print("Training XGBoost Ranker...")
    model = xgb.XGBRanker(
        objective="rank:ndcg",
        ndcg_exp_gain=False,
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        min_child_weight=3,
        random_state=42,
    )
    
    model.fit(
        X=X,
        y=y,
        group=group_sizes,
        verbose=False
    )
    
    model_path = MODELS_DIR / "xgboost_ranker_model.json"
    model.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    with open(MODELS_DIR / "ranker_features.json", "w") as f:
        json.dump(feature_cols, f)

if __name__ == "__main__":
    train_supplier_ranking()
