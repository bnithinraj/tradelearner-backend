from fastapi import FastAPI
from polygon_utils import get_price
import os
import uvicorn

app = FastAPI()

# A+ Scanner Logic
def score_a_plus_setup(price_data):
    price = price_data.get("polygon_data", {}).get("results", {}).get("p")
    volume = price_data.get("polygon_data", {}).get("results", {}).get("v", 0)

    # Basic mock A+ rules (replace with full rule logic as needed)
    if not price:
        return {"error": "No price data"}
    
    score = {
        "price": price,
        "volume": volume,
        "grade": "A+" if price > 5 and volume > 500000 else "B"
    }
    return score

@app.get("/get_price")
def get_price_endpoint(ticker: str):
    return get_price(ticker)

@app.get("/scan_price")
def scan_price_endpoint(ticker: str):
    price_data = get_price(ticker)
    return score_a_plus_setup(price_data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
