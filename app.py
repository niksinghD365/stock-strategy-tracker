from flask import Flask, render_template, request
from nsetools import Nse
import os
import requests

app = Flask(__name__)

def fetch_nse_price(symbol):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        session.get("https://www.nseindia.com", timeout=5)

        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["priceInfo"]["lastPrice"]
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    price = None
    symbol = ""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        price = fetch_nse_price(symbol)

    return render_template("index.html", price=price, symbol=symbol)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
