import os
import requests
from datetime import datetime

def fetch_latest_price(ticker: str):
    api_key = os.getenv("POLYGON_API_KEY")
    url = f"https://api.polygon.io/v2/last/trade/{ticker}"
    params = {"apiKey": api_key}
    response = requests.get(url)

    return {
        "ticker": ticker,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "polygon_data": response.json() if response.ok else {"error": response.text}
    }
