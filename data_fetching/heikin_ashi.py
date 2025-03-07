from data_fetching.trending_coins import TrendingCoins
from data_fetching.fetch_data import MarketDataFetcher


class HeikinAshiConverter:
    """Converts standard candlestick data to Heikin Ashi format"""

    @staticmethod
    def convert(df):
        df_ha = df.copy()
        df_ha["close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
        df_ha["open"] = (df["open"].shift(1) + df["close"].shift(1)) / 2
        df_ha["high"] = df[["open", "close", "high"]].max(axis=1)
        df_ha["low"] = df[["open", "close", "low"]].min(axis=1)
        df_ha.iloc[0, df.columns.get_loc("open")] = df["open"].iloc[0]
        return df_ha

if __name__ == "__main__":
    trending = TrendingCoins().fetch_trending_coins()
    fetcher = MarketDataFetcher()

    for coin in trending:
        df = fetcher.fetch_ohlcv(coin)
        if df is not None:
            df_ha = HeikinAshiConverter.convert(df)
            print(f"\n🔥 Heikin Ashi for {coin}:")
            print(df_ha.head())
