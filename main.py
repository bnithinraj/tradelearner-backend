from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Get Polygon API key from environment variable
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

@app.get("/public_price")
def get_price(ticker: str):
    """
    Public endpoint to fetch real-time stock price via Polygon.io.
    Example: /public_price?ticker=AAPL
    """
    if not POLYGON_API_KEY:
        return { "error": "Polygon API key not set." }

    url = f"https://api.polygon.io/v2/last/trade/stocks/{ticker}"
    response = requests.get(url, params={"apikey": POLYGON_API_KEY})

    if response.ok:
        try:
            data = response.json()
            return {
                "price": data["results"]["p"],
                "timestamp": data["results"]["t"]
            }
        except Exception:
            return { "error": "Failed to parse Polygon response" }
    else:
        return {
            "error": "Polygon fetch failed",
            "status_code": response.status_code
        }

@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return { "status": "ok" }

@app.get("/")
def index():
    """
    API metadata endpoint.
    """
    return {
        "service": "Live Polygon Stock Price API",
        "routes": {
            "/public_price": "Fetch stock price: ?ticker=AAPL",
            "/health": "Health check route"
        }
    }
