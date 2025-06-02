import os
import requests
from flask import jsonify, request

def handler(req):
    try:
        symbol = req.args.get("symbol", "AAPL").upper()
        api_key = os.getenv("POLYGON_API_KEY")
        if not api_key:
            return jsonify({"error": "Missing POLYGON_API_KEY"}), 500

        url = f"https://api.polygon.io/v2/last/trade/{symbol}?apiKey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch price",
                "status_code": response.status_code,
                "details": response.text
            }), response.status_code

        data = response.json()
        price = data.get("results", {}).get("p")  # 'p' = price
        if price is None:
            return jsonify({"error": "Price not found in response"}), 500

        return jsonify({
            "symbol": symbol,
            "price": price
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

