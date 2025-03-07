import requests

class AlertManager:
    """Sends alerts via Telegram"""

    TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(self, telegram_token, chat_id):
        self.token = telegram_token
        self.chat_id = chat_id

    def send_telegram_alert(self, message):
        """Sends trade alert to Telegram"""
        url = self.TELEGRAM_API_URL.format(token=self.token)
        data = {"chat_id": self.chat_id, "text": message}
        requests.post(url, data=data)
