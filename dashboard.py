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

    # Find the index of the last candle that triggered the signal
    signal_index = len(coin_signal["dates"]) - 1
    signal_x = coin_signal["dates"][signal_index]
    signal_y = coin_signal["close"][signal_index]

    # Define the highlight box coordinates
    box_shape = {
        "type": "rect",
        "xref": "x",
        "yref": "y",
        "x0": signal_x - 2,  # Small margin around the candlestick
        "x1": signal_x + 2,
        "y0": signal_y * 0.995,  # Small margin around price
        "y1": signal_y * 1.005,
        "line": {
            "color": "green" if coin_signal["trend"] == "bullish" else "red",
            "width": 3
        }
    }

    # Ensure correct format for Plotly Heikin Ashi chart
    chart_data = {
        "data": [
            {
                "x": coin_signal["dates"],
                "open": coin_signal["open"],
                "high": coin_signal["high"],
                "low": coin_signal["low"],
                "close": coin_signal["close"],
                "type": "candlestick",
                "name": "Heikin Ashi Candles"
            }
        ],
        "layout": {
            "title": f"Heikin Ashi Candles for {coin_name}",
            "xaxis": {"title": "Time", "rangeslider": {"visible": False}},
            "yaxis": {"title": "Price"},
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "shapes": [box_shape]  # Add the highlight rectangle
        }
    }

    # return jsonify({"chart": chart_data})


    trend_color = "green-box" if coin_signal["trend"] == "bullish" else "red-box"

    return jsonify({"chart": chart_data, "trend_color": trend_color})

if __name__ == "__main__":
    app.run(debug=True)
