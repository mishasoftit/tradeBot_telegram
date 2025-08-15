# Telegram Trade Bot

A sophisticated trading bot for Telegram that executes trades based on customizable strategies.

## Features

- Real-time trade execution
- Multiple risk management strategies
- Exchange integration (via CCXT)
- Encrypted API key storage
- Docker support

## Installation

```bash
git clone https://github.com/your-username/tg_trade_bot.git
cd tg_trade_bot

# Create .env file from template
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Start the bot
python main.py
```

## Docker Setup
```bash
docker-compose up --build
```

## Configuration
Edit `.env` with your credentials:
- `TELEGRAM_TOKEN`: Bot token from @BotFather
- `ADMIN_IDS`: Comma-separated list of admin user IDs
- `EXCHANGE_API_KEY`/`EXCHANGE_API_SECRET`: Exchange credentials
- `ENCRYPTION_KEY`: Strong key for data encryption (min 32 chars)
- `DATABASE_URL`: Postgres connection string

## Usage
Start the bot and interact via Telegram:
- /start - Begin trading
- /settings - Configure preferences
- /stats - View performance metrics

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
[MIT](LICENSE)