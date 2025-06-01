from fastapi import FastAPI
from polygon_utils import get_price
import uvicorn
import os

app = FastAPI()

@app.get("/get_price")
def get_price_endpoint(ticker: str):
    return get_price(ticker)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)



