import requests

def fetch_from_nse(symbol):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        }

        session = requests.Session()
        session.headers.update(headers)

        session.get("https://www.nseindia.com", timeout=5)  # Set cookie
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        response = session.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        return data["priceInfo"]["lastPrice"]
    except Exception as e:
        print(f"[NSE] Failed: {e}")
        return None


def fetch_from_groww(symbol):
    try:
        url = f"https://groww.in/v1/api/stocks_data?stock_symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        data = response.json()
        return data["ltp"]
    except Exception as e:
        print(f"[Groww] Failed: {e}")
        return None


def get_stock_price(symbol):
    print(f"Trying to fetch price for: {symbol}")
    
    # Try NSE
    price = fetch_from_nse(symbol)
    if price:
        return price, "NSE India"

    # Try Groww
    price = fetch_from_groww(symbol)
    if price:
        return price, "Groww"

    return None, None
