from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import os

app = Flask(__name__)

def get_stock_data(symbol):
    df = yf.download(symbol, period='3mo', interval='1d')
    df.dropna(inplace=True)
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df['Close'].ewm(span=12).mean()
    ema26 = df['Close'].ewm(span=26).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9).mean()

    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    df = None
    symbol = ''
    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        df = get_stock_data(symbol)
    
    return render_template('index.html', df=df, symbol=symbol)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
