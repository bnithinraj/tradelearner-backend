from fastapi import FastAPI
from pydantic import BaseModel
from mongo_logger import log_trade_to_db
from polygon_utils import fetch_latest_price
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app
app = FastAPI()

# Enable CORS so GPT or any web tool can access it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change this to ["https://chat.openai.com"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for logging trades
class TradeEntry(BaseModel):
    ticker: str
    entry: float
    exit: float
    r_multiple: float
    grade: str

# Endpoint to log a trade
@app.post("/log_trade/")
async def log_trade(trade: TradeEntry):
    log_trade_to_db(trade.dict())
    return {"status": "logged", "data": trade.dict()}

# Endpoint to fetch live price
@app.get("/get_price/")
def get_price(ticker: str):
    print(f"✅ GPT hit /get_price for {ticker}")
    return fetch_latest_price(ticker)

