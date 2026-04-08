import yfinance as yf
import pandas as pd
import requests
import os

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
except ImportError:
    pass

FRED_API_KEY = os.environ.get('FRED_API_KEY')

def fetch_fred_series(series_id: str, start_date: str, end_date: str) -> pd.Series:
    if not FRED_API_KEY:
        print(f"[Warning] No FRED_API_KEY found, returning empty series for {series_id}")
        return pd.Series(dtype=float, name=series_id)

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        observations = data.get("observations", [])
        
        dates = []
        values = []
        for obs in observations:
            val = obs.get("value")
            if val and val != ".":
                dates.append(obs["date"])
                values.append(float(val))
                
        series = pd.Series(values, index=pd.to_datetime(dates), name=series_id)
        return series
    except Exception as e:
        print(f"[Error] Failed to fetch {series_id} from FRED: {e}")
        return pd.Series(dtype=float, name=series_id)

def load_historical_data(start_date: str, end_date: str) -> pd.DataFrame:
    print(f"[DataLoader] Fetching market data from {start_date} to {end_date}...")
    
    tickers = ["QQQ", "SPY", "^VIX", "^TNX"]
    raw_yf = yf.download(tickers, start=start_date, end=end_date, progress=False)
    
    # Check if 'Adj Close' exists, else use 'Close'
    if 'Adj Close' in raw_yf.columns.get_level_values(0):
        yf_data = raw_yf['Adj Close'].copy()
    else:
        yf_data = raw_yf['Close'].copy()
    
    # Rename columns to standardized keys
    yf_data.rename(columns={
        "QQQ": "QQQ_CLOSE",
        "SPY": "SPY_CLOSE",
        "^VIX": "VIX",
        "^TNX": "10Y_YIELD"
    }, inplace=True)
    
    print("[DataLoader] Fetching macro signals from FRED...")
    hy_spread = fetch_fred_series("BAMLH0A0HYM2", start_date, end_date)
    hy_spread.name = "HY_SPREAD"
    
    pmi = fetch_fred_series("ISM/MAN_PMI", start_date, end_date)
    pmi.name = "PMI"
    
    # Merge and Forward Fill
    yf_data.index = pd.to_datetime(yf_data.index).tz_localize(None)
    hy_spread.index = pd.to_datetime(hy_spread.index).tz_localize(None)
    pmi.index = pd.to_datetime(pmi.index).tz_localize(None)
    
    merged = yf_data.join(hy_spread, how="left").join(pmi, how="left")
    merged = merged.ffill() # Forward fill macro data for trading days
    merged = merged.bfill() # Backfill starting NaNs
    
    # Fallbacks for safety
    if "VIX" not in merged.columns or merged["VIX"].isna().all(): merged["VIX"] = 20.0
    if "10Y_YIELD" not in merged.columns or merged["10Y_YIELD"].isna().all(): merged["10Y_YIELD"] = 2.0
    if "HY_SPREAD" not in merged.columns or merged["HY_SPREAD"].isna().all(): merged["HY_SPREAD"] = 4.0
    if "PMI" not in merged.columns or merged["PMI"].isna().all(): merged["PMI"] = 50.0
    
    # Fill remaining NaNs
    merged["VIX"] = merged["VIX"].fillna(20.0)
    merged["10Y_YIELD"] = merged["10Y_YIELD"].fillna(2.0)
    merged["HY_SPREAD"] = merged["HY_SPREAD"].fillna(4.0)
    merged["PMI"] = merged["PMI"].fillna(50.0)
    
    merged.dropna(subset=["QQQ_CLOSE", "SPY_CLOSE"], inplace=True)
    print(f"[DataLoader] Successfully loaded {len(merged)} trading days.")
    return merged

if __name__ == "__main__":
    df = load_historical_data("2020-01-01", "2020-01-31")
    print(df.head())
