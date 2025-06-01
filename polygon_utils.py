import os
import requests

def get_price(ticker):
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        return {"error": "API key missing in environment"}

    url = f"https://api.polygon.io/v2/last/trade/{ticker}?apiKey={api_key}"
    response = requests.get(url)
    return {
        "ticker": ticker,
        "timestamp_utc": response.headers.get("Date"),
        "polygon_data": response.json()
    }
