from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("<h1>📈 Stock Strategy Tracker is Running!</h1>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)