import pandas as pd

class TechnicalIndicators:
    """Class for computing technical indicators like MACD"""

    @staticmethod
    def compute_macd(df, short_window=12, long_window=26, signal_window=9):
        """Computes MACD and Signal Line for a given dataframe"""

        df = df.copy()  # Avoid modifying the original dataframe
        df = df.loc[:, ~df.columns.duplicated()]  # Remove duplicate column names
        df["close"] = pd.to_numeric(df["close"], errors="coerce")  # Ensure numeric values
        df = df.dropna(subset=["close"])  # Remove NaNs if conversion fails

        df["ema_short"] = df["close"].ewm(span=short_window, adjust=False).mean()
        df["ema_long"] = df["close"].ewm(span=long_window, adjust=False).mean()
        df["macd"] = df["ema_short"] - df["ema_long"]
        df["macd_signal"] = df["macd"].ewm(span=signal_window, adjust=False).mean()

        return df


    @staticmethod
    def is_macd_bullish_crossover(df, threshold=5):  # Increased threshold
        """Checks for bullish MACD crossover"""
        return df["macd"].iloc[-1] > df["macd_signal"].iloc[-1] and (
            abs(df["macd"].iloc[-1] - df["macd_signal"].iloc[-1]) < threshold
        )

    @staticmethod
    def is_macd_bearish_crossover(df, threshold=5):  # Increased threshold
        """Checks for bearish MACD crossover"""
        return df["macd"].iloc[-1] < df["macd_signal"].iloc[-1] and (
            abs(df["macd"].iloc[-1] - df["macd_signal"].iloc[-1]) < threshold
        )

    @staticmethod
    def detect_heikin_ashi_trend(df):
        """Determines Heikin Ashi trend"""
        df["ha_diff"] = df["close"] - df["open"]
        bullish_candles = (df["ha_diff"] > 0).sum()
        bearish_candles = (df["ha_diff"] < 0).sum()

        if bullish_candles > bearish_candles:
            return "Bullish" if bullish_candles > 1.5 * bearish_candles else "Weak Bullish"
        elif bearish_candles > bullish_candles:
            return "Bearish" if bearish_candles > 1.5 * bullish_candles else "Weak Bearish"
        else:
            return "Neutral"
