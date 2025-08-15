import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.core import TradingBot
from database.crud import CRUD
from config.settings import Config

class AlertSystem:
    def __init__(self, bot: TradingBot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.check_balance, 'interval', minutes=30)
        self.scheduler.add_job(self.check_strategies, 'interval', hours=1)
        self.scheduler.add_job(self.check_system_health, 'interval', minutes=15)

    async def start(self):
        self.scheduler.start()
        logging.info("Alert system started")

    async def send_alert(self, user_id, message):
        await self.bot.bot.send_message(user_id, f"⚠️ ALERT: {message}")

    async def check_balance(self):
        # Check user balances and notify if below threshold
        users = CRUD.get_all_users()
        for user in users:
            strategy = CRUD.get_active_strategy(user.id)
            if strategy and strategy.capital < strategy.min_capital * 0.9:
                await self.send_alert(
                    user.telegram_id,
                    f"Low balance on {strategy.name} strategy: ${strategy.capital:.2f}"
                )

    async def check_strategies(self):
        # Check for inactive strategies
        users = CRUD.get_all_users()
        for user in users:
            if not CRUD.get_active_strategy(user.id):
                await self.send_alert(
                    user.telegram_id,
                    "No active trading strategy. Please start a strategy."
                )

    async def check_system_health(self):
        # Basic system health check
        if not self.bot.dp.running:
            for admin_id in Config.ADMIN_IDS:
                await self.send_alert(admin_id, "Trading bot is not running!")