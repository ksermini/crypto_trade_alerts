import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailAlerts:
    """Handles sending email alerts for trade signals"""

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("EMAIL_SENDER")  # Store in environment variables
        self.sender_password = os.getenv("EMAIL_PASSWORD")  # Store securely!
        self.recipient_email = os.getenv("EMAIL_RECIPIENT")  # Set recipient
        
    def send_email(self, subject, message):
        """Send an email with the given subject and message"""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            # Connect to email server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email alert sent: {subject}")

        except Exception as e:
            print(f"❌ Failed to send email: {e}")

    def send_trade_signal_alert(self, trade_signals):
        """Send an intra-day email alert for new trade signals"""
        if not trade_signals:
            return  # No signals, no email

        subject = "📈 Trade Signal Alert!"
        message = "🚀 New Trade Signals Detected:\n\n"

        for signal in trade_signals:
            message += f"🔹 {signal['coin']} → {signal['action']} at ${signal['price']:.2f}\n"

        self.send_email(subject, message)

    def send_eod_summary(self, trade_signals):
        """Send an end-of-day summary email"""
        subject = "📊 EOD Trade Summary Report"
        message = "📈 Today's Trade Signals:\n\n"

        if not trade_signals:
            message += "⚠️ No trade signals detected today. Market may have been flat."
        else:
            for signal in trade_signals:
                message += f"🔹 {signal['coin']} → {signal['action']} at ${signal['price']:.2f}\n"

        self.send_email(subject, message)
