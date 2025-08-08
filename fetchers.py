import requests
import yfinance as yf

def get_stock_price(symbol):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 1. Try NSE unofficial API
    try:
        nse_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(nse_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        price = data["priceInfo"]["lastPrice"]
        return price, "NSE"
    except Exception as e:
        print(f"[NSE ERROR] {e}")

    # 2. Fallback to Yahoo Finance
    try:
        ticker = yf.Ticker(symbol + ".NS")
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = hist["Close"].iloc[-1]
            return round(price, 2), "Yahoo Finance"
    except Exception as e:
        print(f"[Yahoo ERROR] {e}")

    # ❌ All failed
    return None, None
