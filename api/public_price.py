import os
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()


async def fetch_latest_price(symbol: str):
    api_key = os.environ.get("POLYGON_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing POLYGON_API_KEY")

    url = f"https://api.polygon.io/v2/last/trade/{symbol}"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params={"apiKey": api_key})

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail={
                "error": "Failed to fetch price",
                "status_code": res.status_code,
                "details": res.text,
            },
        )

    data = res.json()
    result = data.get("results", {})
    price = result.get("p")
    if price is None:
        raise HTTPException(status_code=500, detail="Price not found in Polygon response")

    return {
        "symbol": symbol,
        "price": price,
        "timestamp": result.get("t"),
    }


@app.get("/api/public_price")
async def public_price(symbol: str = "AAPL"):
    return await fetch_latest_price(symbol.upper())


@app.get("/get_price")
@app.get("/get_price/")
async def get_price(ticker: Optional[str] = None, symbol: Optional[str] = None):
    requested_symbol = (ticker or symbol or "AAPL").upper()
    return await fetch_latest_price(requested_symbol)
