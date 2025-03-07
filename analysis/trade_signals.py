from analysis.indicators import TechnicalIndicators
from data_fetching.heikin_ashi import HeikinAshiConverter
from data_fetching.fetch_data import MarketDataFetcher
from data_fetching.trending_coins import TrendingCoins

print("🚀 Starting Trade Signal Detection...")  # Debugging Start

class TradeSignalDetector:
    """Detects trade signals based on MACD and Heikin Ashi trends"""

    def __init__(self):
        print("📊 Initializing TradeSignalDetector...")  # Debugging
        self.fetcher = MarketDataFetcher()
        self.trending = TrendingCoins().fetch_trending_coins()
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

            # Debugging Heikin Ashi trend detection
            print(f"📊 Heikin Ashi Strength for {coin} (last 5 entries):")
            print(df_ha[["close", "open"]].tail(5))

            # Compute MACD
            print(f"📊 Computing MACD for {coin}...")  # Debugging
            df_macd = TechnicalIndicators.compute_macd(df_ha)

            # Check for trade signals
            print(f"\n📊 MACD & Signal Line for {coin} (Last 10 Entries):")
            print(df_macd[["macd", "macd_signal"]].tail(10))

            if TechnicalIndicators.is_macd_bullish_crossover(df_macd):
                print(f"✅ BUY signal detected for {coin}")  # Debugging
                signals.append({"coin": coin, "action": "BUY", "price": df_macd['close'].iloc[-1]})

            elif TechnicalIndicators.is_macd_bearish_crossover(df_macd):
                print(f"❌ SELL signal detected for {coin}")  # Debugging
                signals.append({"coin": coin, "action": "SELL", "price": df_macd['close'].iloc[-1]})

        print("✅ Trade Signal Detection Complete!")  # Debugging
        return signals

if __name__ == "__main__":
    detector = TradeSignalDetector()
    trade_signals = detector.detect_trade_signals()
    
    print("\n🚀 Final Detected Trade Signals:")
    if trade_signals:
        for signal in trade_signals:
            print(f"{signal['coin']} → {signal['action']} at ${signal['price']:.2f}")
    else:
        print("⚠️ No trade signals detected. Market may be flat.")
