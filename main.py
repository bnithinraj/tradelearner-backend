from fastapi import FastAPI, Request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from polygon_utils import fetch_latest_price

load_dotenv()
app = FastAPI()

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["tradelearner"]
log_collection = db["executions"]

@app.post("/log_trade/")
async def log_trade(request: Request):
    trade_data = await request.json()
    log_collection.insert_one(trade_data)
    return {"status": "logged", "data": trade_data}

@app.get("/get_price/")
def get_price(ticker: str):
    result = fetch_latest_price(ticker)
    return result
