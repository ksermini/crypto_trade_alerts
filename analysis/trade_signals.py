from notifications.telegram_alerts import TelegramAlerts
from datetime import datetime
from data_fetching.fetch_data import MarketDataFetcher
from data_fetching.heikin_ashi import HeikinAshiConverter
from analysis.indicators import TechnicalIndicators
from data_fetching.trending_coins import TrendingCoins

class TradeSignalDetector:
    """Detects trade signals based on MACD and Heikin Ashi trends."""

    def __init__(self):
        print("📊 Initializing TradeSignalDetector...")
        self.fetcher = MarketDataFetcher()
        self.telegram_alerts = TelegramAlerts()
        self.signals = []

    def detect_trade_signals(self):
        """Identifies potential buy/sell signals and sends alerts via Telegram."""
        print("📈 Detecting trade signals...")
        self.signals = []

        for coin in TrendingCoins().fetch_trending_coins():
            print(f"🔍 Fetching data for {coin}...")
            df = self.fetcher.fetch_ohlcv(coin)
            if df is None or len(df) < 30:
                print(f"⚠️ Skipping {coin} due to insufficient data.")
                continue

            print(f"🔥 Converting {coin} to Heikin Ashi format...")
            df_ha = HeikinAshiConverter.convert(df)
            print(f"📊 Computing MACD for {coin}...")
            df_macd = TechnicalIndicators.compute_macd(df_ha)

            # Check for trade signals
            if TechnicalIndicators.is_macd_bullish_crossover(df_macd):
                signal = {
                    "coin": coin,
                    "action": "BUY",
                    "price": df_macd['close'].iloc[-1],
                    "dates": df_macd.index.tolist(),
                    "open": df_macd['open'].tolist(),
                    "high": df_macd['high'].tolist(),
                    "low": df_macd['low'].tolist(),
                    "close": df_macd['close'].tolist(),
                    "trend": "bullish",
                    "strength": 5  # Placeholder for scoring
                }
                self.signals.append(signal)
                self.send_intra_alert(signal)

            elif TechnicalIndicators.is_macd_bearish_crossover(df_macd):
                signal = {
                    "coin": coin,
                    "action": "SELL",
                    "price": df_macd['close'].iloc[-1],
                    "dates": df_macd.index.tolist(),
                    "open": df_macd['open'].tolist(),
                    "high": df_macd['high'].tolist(),
                    "low": df_macd['low'].tolist(),
                    "close": df_macd['close'].tolist(),
                    "trend": "bearish",
                    "strength": 2
                }
                self.signals.append(signal)
                self.send_intra_alert(signal)

        # Send EOD summary if it's late at night
        now = datetime.now().strftime("%H:%M")
        if self.signals and now >= "01:00":
            self.send_eod_summary()

        print("✅ Trade Signal Detection Complete!")
        return self.signals

    def send_intra_alert(self, signal):
        """Send intra-day alerts when a trade signal is detected."""
        message = f"🚀 *{signal['coin']} Trade Signal* 🚀\n"
        message += f"🔹 *{signal['action']} Signal Detected*\n"
        message += f"🔹 *Entry Price:* ${signal['price']:.2f}\n"
        message += f"🔹 *Strategy:* MACD + Heikin Ashi Confirmation\n"
        message += "📈 *Trend Indication:* Bullish ✅\n" if signal["trend"] == "bullish" else "📉 *Trend Indication:* Bearish ❌\n"

        print(f"📡 Sending intra-day alert: {message}")
        self.telegram_alerts.send_alert(message)

    def send_eod_summary(self):
        """Send the End-of-Day summary with trading performance."""
        now = datetime.utcnow().strftime("%B %d, %Y")
        summary_message = f"📊 *End-of-Day Trading Summary* 📊\n(Generated on: {now})\n\n---\n"

        for i, signal in enumerate(self.signals):
            summary_message += f"💰 *Trade #{i + 1}: {signal['coin']}*\n"
            summary_message += f"{'✅ *Good Trade*' if signal['strength'] >= 4 else '❌ *Bad Trade*'}\n"
            summary_message += f"🕒 *Trade Executed:* {now} UTC\n"
            summary_message += f"🔹 *Entry Price:* ${signal['price']:.2f}\n"
            summary_message += "---\n"

        summary_message += f"\n📈 *Performance Summary:*\n"
        summary_message += f"✅ *Total Trades:* {len(self.signals)}\n"

        print(f"📡 Sending EOD Summary:\n{summary_message}")
        self.telegram_alerts.send_alert(summary_message)


if __name__ == "__main__":
    detector = TradeSignalDetector()
    detector.detect_trade_signals()
