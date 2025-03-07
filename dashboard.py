from flask import Flask, render_template, jsonify
import json
from analysis.trade_signals import TradeSignalDetector  

app = Flask(__name__)

# Initialize trade signal detector
detector = TradeSignalDetector()
signals = detector.detect_trade_signals()

# Process best and top 5 signals
best_signal = max(signals, key=lambda x: x.get("strength", 0), default=None)
top_signals = sorted(signals, key=lambda x: x.get("strength", 0), reverse=True)[:5]

@app.route("/")
def index():
    """Render main dashboard page with the best signal and top 5 trending coins."""
    return render_template("index.html", best_signal=best_signal, top_signals=top_signals)

@app.route("/coin/<coin_name>")
def get_coin_data(coin_name):
    """Fetch Heikin Ashi data and trend color for a specific coin."""
    coin_signal = next((s for s in signals if s["coin"] == coin_name), None)
    if not coin_signal:
        return jsonify({"error": "Coin not found"}), 404

    print(f"🔍 Debugging Coin Data for {coin_name}: {coin_signal}")  # Debugging

    # Ensure correct format for Plotly
    chart_data = {
        "data": [{
            "x": list(range(len(coin_signal["dates"]))),  # Ensure X-axis values are numeric
            "open": coin_signal["open"],
            "high": coin_signal["high"],
            "low": coin_signal["low"],
            "close": coin_signal["close"],
            "type": "candlestick"
        }],
        "layout": {
            "title": f"Heikin Ashi Candles for {coin_name}",
            "xaxis": {"title": "Time", "rangeslider": {"visible": False}},  # Ensure x-axis shows time
            "yaxis": {"title": "Price"},
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)"
        }
    }

    trend_color = "green-box" if coin_signal["trend"] == "bullish" else "red-box"

    return jsonify({"chart": chart_data, "trend_color": trend_color})

if __name__ == "__main__":
    app.run(debug=True)
