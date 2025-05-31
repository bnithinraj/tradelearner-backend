from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["tradelearner"]
log_collection = db["executions"]

def log_trade_to_db(trade_data: dict):
    log_collection.insert_one(trade_data)
