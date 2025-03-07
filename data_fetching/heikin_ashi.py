import pandas as pd

class HeikinAshiConverter:
    """Class to convert standard candlestick data to Heikin Ashi format"""

    @staticmethod
    def convert(df):
        """Convert OHLCV dataframe to Heikin Ashi format"""

        # Create a copy to avoid modifying original data
        df_ha = df.copy()

        # Compute Heikin Ashi Close
        df_ha["ha_close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4

        # Compute Heikin Ashi Open (shifted by one row)
        df_ha["ha_open"] = (df["open"].shift(1) + df["close"].shift(1)) / 2

        # Fill the first row to avoid NaN values
        df_ha.loc[df_ha.index[0], "ha_open"] = df.loc[df.index[0], "open"]

        # Compute Heikin Ashi High & Low
        df_ha["ha_high"] = df_ha[["ha_open", "ha_close", "high"]].max(axis=1)
        df_ha["ha_low"] = df_ha[["ha_open", "ha_close", "low"]].min(axis=1)

        # Drop NaN values (if any)
        df_ha = df_ha.dropna()

        # Rename columns to match original format
        df_ha.rename(columns={"ha_open": "open", "ha_close": "close", "ha_high": "high", "ha_low": "low"}, inplace=True)

        return df_ha
