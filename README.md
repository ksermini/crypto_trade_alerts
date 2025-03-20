# Crypto Trade Alerts

*An automated system for monitoring cryptocurrency markets and sending trade alerts.*

## Overview

Crypto Trade Alerts is a Python-based application designed to monitor cryptocurrency markets and notify users of potential trading opportunities. The system fetches real-time market data, analyzes it based on predefined strategies, and sends alerts through email and Telegram.

## Features

- **Data Fetching**: Retrieves real-time cryptocurrency market data.
- **Analysis**: Applies trading strategies to identify potential opportunities.
- **Notifications**: Sends alerts via email and Telegram.
- **Simulation**: Simulates trades to evaluate strategy performance.
- **Web Dashboard**: Provides a web-based interface to monitor system status and alerts.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ksermini/crypto_trade_alerts.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd crypto_trade_alerts
   ```

3. **Create and activate a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables to configure the notification system:

```bash
EMAIL_SENDER="your_email@example.com"
EMAIL_PASSWORD="your_email_password"
EMAIL_RECIPIENT="recipient_email@example.com"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_CHAT_ID="your_telegram_chat_id"
```

Replace the placeholder values with your actual credentials.

## Usage

1. **Fetch Data**: Execute the data fetching module to retrieve market data.
2. **Analyze Data**: Run the analysis module to process the fetched data and identify trading signals.
3. **Send Notifications**: The system will automatically send notifications based on the analysis results.
4. **Simulate Trades**: Use the simulation module to backtest trading strategies.
5. **Web Dashboard**: Launch the web dashboard to monitor system status and view alerts.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Disclaimer

This system is intended for informational purposes only and does not constitute financial advice. Use it at your own risk.
