import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "ml" / "models"
os.makedirs(MODELS_DIR, exist_ok=True)

def train_and_predict_anomalies():
    print("Loading data for Anomaly Detection (Model 4)...")
    df = pd.read_csv(DATA_DIR / "brent_price_monthly.csv", parse_dates=["date"])
    
    # Feature Engineering (Isolation Forest features)
    df["volatility_6m"] = df["price"].rolling(6, min_periods=3).std()
    df["momentum_6m"] = df["price"].pct_change(6) * 100
    df["price_max_3m"] = df["price"].rolling(3, min_periods=1).max()
    df["price_min_3m"] = df["price"].rolling(3, min_periods=1).min()
    # Avoid division by zero
    df["price_range_3m"] = (df["price_max_3m"] - df["price_min_3m"]) / df["rolling_avg_3m"].replace(0, np.nan)
    
    # Fill NAs from rolling for the earliest rows to avoid dropping them
    df.bfill(inplace=True)
    df.fillna(0, inplace=True)

    feature_cols = [
        "price", "price_change_pct", "rolling_avg_3m", "rolling_std_3m",
        "price_zscore", "volatility_6m", "momentum_6m", "price_range_3m"
    ]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    
    print("Training Isolation Forest...")
    model = IsolationForest(
        n_estimators=200,
        max_samples="auto",
        contamination=0.05,
        max_features=1.0,
        bootstrap=False,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled)
    
    df["anomaly_flag"] = model.predict(X_scaled)
    df["anomaly_score"] = model.decision_function(X_scaled)
    df["is_anomaly"] = df["anomaly_flag"] == -1
    
    # Save the output to a JSON file to be easily read by dashboard.py
    output_records = df.to_dict(orient="records")
    # Date formatting
    for record in output_records:
        record["date"] = record["date"].strftime("%Y-%m-%d")
        record["anomaly_flag"] = bool(record["is_anomaly"])
        # Avoid non-serializable types
        for k, v in record.items():
            if pd.isna(v):
                record[k] = None
    
    output_path = DATA_DIR / "brent_anomalies_output.json"
    with open(output_path, "w") as f:
        json.dump(output_records, f, indent=2)
    
    print(f"Anomaly detection complete. Results saved to {output_path}")

if __name__ == "__main__":
    train_and_predict_anomalies()
