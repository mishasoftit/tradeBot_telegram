import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import Config

class TradingBot:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_TOKEN)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self._register_handlers()
        logging.basicConfig(level=Config.LOG_LEVEL)

    def _register_handlers(self):
        from bot.handlers.start import register_start_handlers
        register_start_handlers(self.dp)
        
        # Future handler registrations will go here

    async def start(self):
        try:
            logging.info("Starting trading bot")
            await self.dp.start_polling()
        finally:
            await self.bot.close()