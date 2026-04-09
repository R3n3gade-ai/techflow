import yfinance as yf
from datetime import datetime, timedelta

def get_performance_vs_qqq(ticker: str, days_back: int = 45):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back + 10) # Buffer for weekends/holidays
        
        # Download data
        data = yf.download(f"{ticker} QQQ", start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), progress=False)
        if data.empty:
            return None
            
        # Get actual trading days
        prices = data['Close']
        if len(prices) < 2:
            return None
            
        # Get start and end prices
        # Find the row closest to 'days_back' trading days ago
        target_idx = max(0, len(prices) - days_back)
        
        pos_start = float(prices[ticker].iloc[target_idx])
        qqq_start = float(prices['QQQ'].iloc[target_idx])
        
        pos_end = float(prices[ticker].iloc[-1])
        qqq_end = float(prices['QQQ'].iloc[-1])
        
        pos_return = (pos_end / pos_start) - 1.0
        qqq_return = (qqq_end / qqq_start) - 1.0
        
        underperf = max(0.0, (qqq_return - pos_return) * 100.0)
        
        return {
            "ticker": ticker,
            "days_back": days_back,
            "qqq_return": round(qqq_return * 100, 2),
            "pos_return": round(pos_return * 100, 2),
            "underperf_pp": round(underperf, 2)
        }
    except Exception as e:
        print(f"Error fetching Yahoo Finance data: {e}")
        return None

res = get_performance_vs_qqq("ALAB", 45)
print(res)
