import pandas as pd

class TechnicalIndicators:
    """Provides methods for computing MACD, detecting trends, and trade signals."""

    @staticmethod
    def compute_macd(df, short_window=12, long_window=26, signal_window=9):
        """
        Computes the MACD (Moving Average Convergence Divergence) indicator.

        Parameters:
        df (DataFrame): A DataFrame containing the 'close' price.
        short_window (int): The period for the short EMA (default: 12).
        long_window (int): The period for the long EMA (default: 26).
        signal_window (int): The period for the signal line (default: 9).

        Returns:
        DataFrame: DataFrame with 'macd' and 'macd_signal' columns added.
        """
        df["ema_short"] = df["close"].ewm(span=short_window, adjust=False).mean()
        df["ema_long"] = df["close"].ewm(span=long_window, adjust=False).mean()
        df["macd"] = df["ema_short"] - df["ema_long"]
        df["macd_signal"] = df["macd"].ewm(span=signal_window, adjust=False).mean()
        
        return df

    @staticmethod
    def is_macd_bullish_crossover(df, threshold=0.01):
        """
        Detects if MACD has a bullish crossover (MACD line crosses above Signal line).

        Parameters:
        df (DataFrame): DataFrame containing 'macd' and 'macd_signal'.
        threshold (float): Minimum difference to detect a weak crossover.

        Returns:
        bool: True if a bullish crossover occurs, otherwise False.
        """
        return (df["macd"].iloc[-2] < df["macd_signal"].iloc[-2] and
                df["macd"].iloc[-1] > df["macd_signal"].iloc[-1]) or \
               (abs(df["macd"].iloc[-1] - df["macd_signal"].iloc[-1]) < threshold)

    @staticmethod
    def is_macd_bearish_crossover(df, threshold=0.01):
        """
        Detects if MACD has a bearish crossover (MACD line crosses below Signal line).

        Parameters:
        df (DataFrame): DataFrame containing 'macd' and 'macd_signal'.
        threshold (float): Minimum difference to detect a weak crossover.

        Returns:
        bool: True if a bearish crossover occurs, otherwise False.
        """
        return (df["macd"].iloc[-2] > df["macd_signal"].iloc[-2] and
                df["macd"].iloc[-1] < df["macd_signal"].iloc[-1]) or \
               (abs(df["macd"].iloc[-1] - df["macd_signal"].iloc[-1]) < threshold)

    @staticmethod
    def detect_heikin_ashi_trend(df):
        """
        Detects the trend using Heikin Ashi candles.

        Parameters:
        df (DataFrame): A DataFrame containing 'open', 'close', 'high', 'low' prices.

        Returns:
        str: "Bullish" if uptrend, "Bearish" if downtrend, "Neutral" otherwise.
        """
        last_ha_close = df["close"].iloc[-1]
        prev_ha_close = df["close"].iloc[-2]

        last_ha_open = df["open"].iloc[-1]
        prev_ha_open = df["open"].iloc[-2]

        # Bullish Trend (Higher HA Close & Open)
        if last_ha_close > prev_ha_close and last_ha_open > prev_ha_open:
            return "Bullish"

        # Bearish Trend (Lower HA Close & Open)
        elif last_ha_close < prev_ha_close and last_ha_open < prev_ha_open:
            return "Bearish"

        # Neutral Trend (Sideways movement)
        return "Neutral"

    @staticmethod
    def detect_trade_signals(df_macd, df_ha):
        """
        Identifies trade signals based on MACD crossovers and Heikin Ashi trends.

        Parameters:
        df_macd (DataFrame): DataFrame with 'macd' and 'macd_signal' columns.
        df_ha (DataFrame): DataFrame with Heikin Ashi candles.

        Returns:
        str: "BUY" if a bullish signal is detected, "SELL" for bearish, else None.
        """
        macd_bullish = TechnicalIndicators.is_macd_bullish_crossover(df_macd)
        macd_bearish = TechnicalIndicators.is_macd_bearish_crossover(df_macd)
        ha_trend = TechnicalIndicators.detect_heikin_ashi_trend(df_ha)

        if macd_bullish and ha_trend == "Bullish":
            return "BUY"
        elif macd_bearish and ha_trend == "Bearish":
            return "SELL"

        return None
