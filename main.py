#!/usr/bin/env python3
"""
Main entry point for the trading bot application
"""
import asyncio
from bot.core import TradingBot

async def main():
    """Initialize and run the trading bot"""
    bot = TradingBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())