import os
import pandas as pd
from prophet import Prophet
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "ml" / "models"
os.makedirs(MODELS_DIR, exist_ok=True)

def train_and_forecast_demand():
    print("Loading data for Demand Forecasting (Model 3)...")
    df = pd.read_csv(DATA_DIR / "prophet_crude_import_tmt.csv")
    df['ds'] = pd.to_datetime(df['ds'])
    
    gdp = pd.read_csv(DATA_DIR / "india_gdp_cleaned.csv")
    gdp["ds"] = pd.to_datetime(gdp["ds"])
    
    # Merge GDP on year
    df = df.merge(
        gdp[["ds", "gdp_growth_rate"]].rename(columns={"ds": "ds_gdp"}),
        left_on=df["ds"].dt.year,
        right_on=gdp["ds"].dt.year,
        how="left"
    )
    df.drop(columns=["key_0", "ds_gdp"], inplace=True, errors='ignore')
    # Fill NAs
    df.ffill(inplace=True)
    df.fillna(0, inplace=True)

    print("Training Prophet Model...")
    model = Prophet(
        growth="linear",
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.1,
        seasonality_mode="multiplicative",
        interval_width=0.80,
    )
    
    model.add_regressor("gdp_growth_rate", mode="multiplicative")
    model.fit(df)
    
    # Make future dataframe for 3 years
    future = model.make_future_dataframe(periods=3, freq="YS")
    # For future periods, forward fill the last known GDP growth rate
    future['year'] = future['ds'].dt.year
    gdp_years = gdp.copy()
    gdp_years['year'] = gdp_years['ds'].dt.year
    future = pd.merge(future, gdp_years[['year', 'gdp_growth_rate']], on='year', how='left')
    future['gdp_growth_rate'] = future['gdp_growth_rate'].ffill().bfill()
    future.drop(columns=['year'], inplace=True)
    
    print("Forecasting...")
    forecast = model.predict(future)
    
    # Extract only future forecasts or last few points for dashboard
    forecast['forecasted_demand_bpd'] = (forecast['yhat'] * 1000 * 7.33) / 365
    forecast['forecast_lower_bpd'] = (forecast['yhat_lower'] * 1000 * 7.33) / 365
    forecast['forecast_upper_bpd'] = (forecast['yhat_upper'] * 1000 * 7.33) / 365
    
    # Let's save the last 5 years + 3 years future
    tail_forecast = forecast.tail(8).copy()
    
    output_records = []
    for _, row in tail_forecast.iterrows():
        output_records.append({
            "date": row["ds"].strftime("%Y-%m-%d"),
            "forecasted_demand_tmt": float(row["yhat"]),
            "forecast_lower": float(row["yhat_lower"]),
            "forecast_upper": float(row["yhat_upper"]),
            "forecasted_demand_bpd": int(row["forecasted_demand_bpd"]),
            "forecast_lower_bpd": int(row["forecast_lower_bpd"]),
            "forecast_upper_bpd": int(row["forecast_upper_bpd"]),
        })
    
    output_data = {
        "forecast": output_records,
        "model_metadata": {
            "training_periods": len(df),
            "regressor": "gdp_growth_rate",
            "last_training_date": df['ds'].max().strftime("%Y-%m-%d")
        }
    }
    
    output_path = DATA_DIR / "prophet_forecast_output.json"
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Demand forecasting complete. Results saved to {output_path}")

if __name__ == "__main__":
    train_and_forecast_demand()
