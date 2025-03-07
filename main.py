from analysis.trade_signals import TradeSignalDetector

if __name__ == "__main__":
    print("🚀 Running Crypto Trade Alert System...")

    detector = TradeSignalDetector()
    trade_signals = detector.detect_trade_signals()

    print("\n🚀 Final Detected Trade Signals:")
    if trade_signals:
        for signal in trade_signals:
            print(f"{signal['coin']} → {signal['action']} at ${signal['price']:.2f}")
    else:
        print("⚠️ No trade signals detected. Market may be flat.")
