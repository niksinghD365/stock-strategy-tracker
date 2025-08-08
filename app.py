from flask import Flask, render_template, request
import os
import requests
from fetchers import get_stock_price

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    price = None
    source = None
    error = None

    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        price, source = get_stock_price(symbol)

        if not price:
            error = f"❌ Failed to fetch price for '{symbol}'. Please check the symbol or try later."

    return render_template("index.html", price=price, source=source, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
