from analysis.trade_signals import TradeSignalDetector
from notifications.email_notifier import EmailNotifier
from notifications.telegram_notifier import TelegramNotifier
from ui.dashboard import CryptoDashboard

def main():
    print("🚀 Running Crypto Trade Alert System...")
    
    # Run Trade Signal Detection
    detector = TradeSignalDetector()
    trade_signals = detector.detect_trade_signals()

    # Notify if signals are found
    if trade_signals:
        EmailNotifier.send_trade_alerts(trade_signals)
        TelegramNotifier.send_trade_alerts(trade_signals)
    
    # Start the UI Dashboard
    CryptoDashboard.run()

if __name__ == "__main__":
    main()
