from flask import Flask, render_template, request
from nsetools import Nse
import os

app = Flask(__name__)

def get_nse_stock_data(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol.upper()}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol.upper()}",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

    session = requests.Session()
    session.headers.update(headers)

    # Necessary: NSE blocks without visiting homepage first
    session.get("https://www.nseindia.com", timeout=5)

    response = session.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()
        return {
            "symbol": data["symbol"],
            "lastPrice": data["priceInfo"]["lastPrice"],
            "dayHigh": data["priceInfo"]["intraDayHighLow"]["max"],
            "dayLow": data["priceInfo"]["intraDayHighLow"]["min"],
            "previousClose": data["priceInfo"]["previousClose"]
        }
    else:
        return {"error": f"Failed to fetch data for {symbol}"}

@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    error = None

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        try:
            stock_data = get_nse_stock_data(symbol)
            if "error" in stock_data:
                error = stock_data["error"]
                stock_data = None
        except Exception as e:
            error = str(e)

    return render_template("index.html", stock_data=stock_data, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
