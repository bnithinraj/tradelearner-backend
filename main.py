from fastapi import FastAPI
import requests
import os

app = FastAPI()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

@app.get("/public_price")
def get_price(ticker: str):
    url = f"https://api.polygon.io/v2/last/trade/stocks/{ticker}"
    response = requests.get(url, params={"apikey": POLYGON_API_KEY})

    if response.ok:
        data = response.json()
        return {
            "price": data["results"]["p"],
            "timestamp": data["results"]["t"]
        }
    else:
        return {
            "error": "Polygon fetch failed",
            "status_code": response.status_code
        }

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/")
def index():
    return {
        "service": "Live Polygon Stock Price API for GPT",
        "status": "running",
        "example": "/public_price?ticker=AAPL"
    }
