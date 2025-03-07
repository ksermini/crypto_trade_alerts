import os
import requests

class TelegramAlerts:
    """Handles sending alerts to a Telegram chat."""

    def __init__(self):
        # Load environment variables
        self.bot_token = "7549688024:AAETD23ByGBxQws9HzksWtc7ZtspJG7PIVM"
        self.chat_ids = [7376632979,7897491592]

        # Debugging output
        print(f"🔍 Debugging Telegram Alerts:")
        print(f"➡️ Bot Token: {self.bot_token}")
        print(f"➡️ Chat ID: {self.chat_ids}")

        if not self.bot_token or not self.chat_ids:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID!")

        # Define the API URL
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_alert(self, message):
        """Sends a message to the configured Telegram chat."""
        # data = {
        #     "chat_id": self.chat_id,
        #     "text": message
        # }

        # print(f"📡 Sending message to Telegram: {data}")  # Debugging output

        # response = requests.post(self.api_url, json=data)
        for chat_id in self.chat_ids:
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
            response = requests.post(self.api_url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Telegram message sent successfully!")
        else:
            print(f"❌ Failed to send Telegram alert: {response.status_code}, {response.text}")



    def send_trade_signal_alert(self, trade_signals):
        """Send an intra-day Telegram alert for new trade signals"""
        if not trade_signals:
            return  # No signals, no alert

        message = "🚀 *New Trade Signals Detected:*\n\n"

        for signal in trade_signals:
            message += f"🔹 *{signal['coin']}* → {signal['action']} at *${signal['price']:.2f}*\n"

        self.send_alert(message)

    def send_eod_summary(self, trade_signals):
        """Send an end-of-day summary Telegram alert"""
        message = "📊 *EOD Trade Summary Report:*\n\n"

        if not trade_signals:
            message += "⚠️ No trade signals detected today. Market may have been flat."
        else:
            for signal in trade_signals:
                message += f"🔹 *{signal['coin']}* → {signal['action']} at *${signal['price']:.2f}*\n"

        self.send_alert(message)


# Run the test
if __name__ == "__main__":
    telegram_alert = TelegramAlerts()
    telegram_alert.send_alert("🚀 Test alert from bot!")