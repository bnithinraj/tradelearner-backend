import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_latest_price(ticker: str):
    url = f"https://api.polygon.io/v2/last/trade/{ticker}"
    params = {"apiKey": os.getenv("POLYGON_API_KEY")}
    response = requests.get(url, params=params)
    return response.json() if response.ok else {"error": response.text}
