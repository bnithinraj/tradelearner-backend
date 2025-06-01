from fastapi import FastAPI
from pydantic import BaseModel
from mongo_logger import log_trade_to_db
from polygon_utils import fetch_latest_price

app = FastAPI()

class TradeEntry(BaseModel):
    ticker: str
    entry: float
    exit: float
    r_multiple: float
    grade: str

@app.post("/log_trade/")
async def log_trade(trade: TradeEntry):
    log_trade_to_db(trade.dict())
    return {"status": "logged", "data": trade.dict()}

@app.get("/get_price/")
def get_price(ticker: str):
    print(f"✅ GPT hit /get_price for {ticker}")  # log to Render
    return fetch_latest_price(ticker)
