import requests
import pandas as pd

COINBASE_CANDLESTICK_URL = "https://api.exchange.coinbase.com/products/{pair}/candles"

class MarketDataFetcher:
    """Fetches OHLCV (candlestick) data for selected crypto pairs"""

    def __init__(self, granularity=300):
        self.granularity = granularity
        print("📡 MarketDataFetcher initialized.")  # Debugging

    def fetch_ohlcv(self, symbol):
        """Fetches OHLCV (candlestick) data for a given symbol"""
        url = COINBASE_CANDLESTICK_URL.format(pair=symbol)
        print(f"🔍 Fetching OHLCV data from {url}")  # Debugging
        params = {"granularity": self.granularity}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"⚠️ Error fetching data for {symbol}: {response.json()}")  # Debugging
            return None

        data = response.json()
        if not data:
            print(f"⚠️ No data returned for {symbol}.")  # Debugging
            return None

        # Convert API response to DataFrame
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
        
        # Convert 'time' to datetime
        df["time"] = pd.to_datetime(df["time"], unit='s')

        # Convert all other columns to float (EXCLUDING 'time')
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)

        print(f"✅ Data fetched for {symbol}: {df.head()}")  # Debugging
        return df
