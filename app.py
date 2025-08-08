from flask import Flask, render_template, request
from nsetools import Nse
import os

app = Flask(__name__)
nse = Nse()

@app.route('/', methods=['GET', 'POST'])
def home():
    stock_data = None
    error = None

    if request.method == 'POST':
        symbol = request.form['symbol'].lower()  # NSE uses lowercase symbols

        try:
            stock_data = nse.get_quote(symbol)
        except Exception as e:
            error = f"Failed to get data for '{symbol.upper()}': {str(e)}"

    return render_template('index.html', stock_data=stock_data, error=error)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
