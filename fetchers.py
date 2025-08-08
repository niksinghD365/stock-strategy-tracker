import requests

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
        data = response.json()
        price = data["priceInfo"]["lastPrice"]
        return price, "NSE"
    except Exception as e:
        print(f"NSE fetch failed: {e}")

    # 2. Try Yahoo Finance fallback
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol + ".NS")
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = hist["Close"].iloc[-1]
            return round(price, 2), "Yahoo Finance"
    except Exception as e:
        print(f"Yahoo fetch failed: {e}")

    # ❌ All failed
    return No
