from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

@app.get("/api/public_price")
async def get_price(symbol: str = "AAPL"):
    api_key = os.environ.get("POLYGON_API_KEY")
    url = f"https://api.polygon.io/v2/last/trade/stocks/{symbol}?apiKey={api_key}"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
    return {
        "symbol": symbol,
        "price": data.get("last", {}).get("price"),
        "timestamp": data.get("last", {}).get("timestamp")
    }
