from analysis.indicators import TechnicalIndicators
from data_fetching.heikin_ashi import HeikinAshiConverter
from data_fetching.fetch_data import MarketDataFetcher
from data_fetching.trending_coins import TrendingCoins
from notifications.email_alerts import EmailAlerts
from notifications.telegram_alerts import TelegramAlerts

print("🚀 Starting Trade Signal Detection...")  # Debugging Start

class TradeSignalDetector:
    """Detects trade signals based on MACD and Heikin Ashi trends"""

    def __init__(self):
        print("📊 Initializing TradeSignalDetector...")  # Debugging
        self.fetcher = MarketDataFetcher()
        self.trending = TrendingCoins().fetch_trending_coins()
        self.email_alerts = EmailAlerts()
        self.telegram_alerts = TelegramAlerts()
        print(f"🔍 Trending Coins: {self.trending}")  # Debugging

    def detect_trade_signals(self):
        """Identifies potential buy/sell signals"""
        print("📈 Detecting trade signals...")  # Debugging
        signals = []

        for coin in self.trending:
            print(f"🔍 Fetching data for {coin}...")  # Debugging
            df = self.fetcher.fetch_ohlcv(coin)

            if df is None or len(df) < 30:
                print(f"⚠️ Skipping {coin} due to insufficient data.")  # Debugging
                continue  # Skip if data is unavailable or too short

            # Convert to Heikin Ashi format
            print(f"🔥 Converting {coin} to Heikin Ashi format...")  # Debugging
            df_ha = HeikinAshiConverter.convert(df)

            # Compute MACD
            print(f"📊 Computing MACD for {coin}...")  # Debugging
            df_macd = TechnicalIndicators.compute_macd(df_ha)

            # Ensure we get the last available close price
            last_close_price = df_macd['close'].iloc[-1] if 'close' in df_macd.columns else None

            signal = None

            # Check for trade signals
            if TechnicalIndicators.is_macd_bullish_crossover(df_macd):
                signal = {"coin": coin, "action": "BUY", "price": last_close_price}
                print(f"✅ BUY signal detected for {coin}")  # Debugging
                self.telegram_alerts.send_alert(f"🚀 Trade Signal: {coin} → **BUY** at ${signal['price']:.2f}")

            elif TechnicalIndicators.is_macd_bearish_crossover(df_macd):
                signal = {"coin": coin, "action": "SELL", "price": last_close_price}
                print(f"❌ SELL signal detected for {coin}")  # Debugging
                self.telegram_alerts.send_alert(f"📉 Trade Signal: {coin} → **SELL** at ${signal['price']:.2f}")

            # Only append the signal if it's valid
            if signal:
                signals.append(signal)

                print("✅ Trade Signal Detection Complete!")  # Debugging

                # 🔴 **Send Intra-Day Alerts**
                # self.email_alerts.send_trade_signal_alert(signals)
                # self.telegram_alerts.send_trade_signal_alert(signals)

                return signals
    def send_eod_summary(self, signals):
        """Sends an end-of-day summary alert via Telegram."""
        if not signals:
            self.telegram_alerts.send_alert("⚠️ No trade signals detected today. Market may be flat.")
        else:
            summary_message = "📊 **End-of-Day Trade Summary** 📊\n\n"
            for signal in signals:
                summary_message += f"🔹 {signal['coin']} → {signal['action']} at ${signal['price']:.2f}\n"

            self.telegram_alerts.send_alert(summary_message)
if __name__ == "__main__":
    detector = TradeSignalDetector()
    trade_signals = detector.detect_trade_signals()

    print("\n🚀 Final Detected Trade Signals:")
    print(f"Signals: {trade_signals}")

    # Send EOD summary after detecting signals
    detector.send_eod_summary(trade_signals)