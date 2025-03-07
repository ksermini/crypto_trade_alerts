import requests
import pandas as pd

COINBASE_API_URL = "https://api.exchange.coinbase.com/products/stats"

class TrendingCoins:
    """Fetches and selects the top 5 trending coins from Coinbase"""

    def __init__(self):
        self.url = COINBASE_API_URL

    def fetch_trending_coins(self, top_n=5):
        """Fetches the top N trending coins based on 24-hour price change & volume"""
        response = requests.get(self.url)
        
        # Print the raw response to debug the issue
        if response.status_code != 200:
            print("Error fetching Coinbase data:", response.json())
            return []

        data = response.json()
        print("\n📊 Sample of API Response:", dict(list(data.items())[:5]))  # Print first 5 items  # Debugging print statement

        # Convert API response to DataFrame
        df = pd.DataFrame.from_dict(data, orient="index")

        # Extract stats_24hour values
        df = df["stats_24hour"].apply(pd.Series)

        # Convert numeric values
        df["price_change_24h"] = pd.to_numeric(df["last"]) - pd.to_numeric(df["open"])
        df["volume"] = pd.to_numeric(df["volume"])

        # Sort coins by highest price movement & volume
        df_sorted = df.sort_values(by=["price_change_24h", "volume"], ascending=[False, False])
        top_coins = df_sorted.index[:top_n].tolist()

        print("\n✅ Trending Coins Selected:", top_coins)  # Debugging statement
        return top_coins

if __name__ == "__main__":
    tc = TrendingCoins()
    top_coins = tc.fetch_trending_coins()
    print("Top 5 Trending Coins (Coinbase):", top_coins)
