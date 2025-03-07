import requests
import os

class TelegramAlerts:
    """Handles sending trade alerts via Telegram"""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Set in environment
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Telegram group or user ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_telegram_message(self, message):
        """Send a message to Telegram"""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise error if request fails
            print(f"✅ Telegram alert sent: {message[:50]}...")  # Print preview

        except Exception as e:
            print(f"❌ Failed to send Telegram alert: {e}")

    def send_trade_signal_alert(self, trade_signals):
        """Send an intra-day Telegram alert for new trade signals"""
        if not trade_signals:
            return  # No signals, no alert

        message = "🚀 *New Trade Signals Detected:*\n\n"

        for signal in trade_signals:
            message += f"🔹 *{signal['coin']}* → {signal['action']} at *${signal['price']:.2f}*\n"

        self.send_telegram_message(message)

    def send_eod_summary(self, trade_signals):
        """Send an end-of-day summary Telegram alert"""
        message = "📊 *EOD Trade Summary Report:*\n\n"

        if not trade_signals:
            message += "⚠️ No trade signals detected today. Market may have been flat."
        else:
            for signal in trade_signals:
                message += f"🔹 *{signal['coin']}* → {signal['action']} at *${signal['price']:.2f}*\n"

        self.send_telegram_message(message)
