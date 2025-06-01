from fastapi import FastAPI
from pydantic import BaseModel
from mongo_logger import log_trade_to_db
from polygon_utils import fetch_latest_price
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

# Allow CORS so GPT can call this backend directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for trade logging
class TradeEntry(BaseModel):
    ticker: str
    entry: float
    exit: float
    r_multiple: float
    grade: str

# MongoDB trade logger
@app.post("/log_trade/")
async def log_trade(trade: TradeEntry):
    log_trade_to_db(trade.dict())
    return {"status": "logged", "data": trade.dict()}

# Live price with timestamp (internal use)
@app.get("/get_price/")
def get_price(ticker: str):
    print(f"✅ GPT hit /get_price for {ticker}")
    return fetch_latest_price(ticker)

# New: Proxy endpoint that fetches Polygon price directly
@app.get("/proxy_price/")
def proxy_price(ticker: str):
    polygon_key = os.getenv("POLYGON_API_KEY")
    url = f"https://api.polygon.io/v2/last/trade/{ticker}?apiKey={polygon_key}"
    response = requests.get(url)
    return response.json()


