import unittest
from unittest.mock import patch, MagicMock
from bot.core import TradeBot

class TestTradeBot(unittest.TestCase):

    @patch('bot.core.Bot')
    def setUp(self, mock_bot):
        self.bot = TradeBot()
        self.bot.bot = mock_bot

    @patch('bot.core.Dispatcher')
    def test_init(self, mock_dispatcher):
        self.assertIsNotNone(self.bot.bot)
        self.assertIsNotNone(self.bot.dp)

    @patch('bot.handlers.start.register_handlers')
    def test_register_handlers(self, mock_register):
        self.bot.register_handlers()
        mock_register.assert_called_once_with(self.bot.dp)

    @patch('bot.core.executor.start_polling')
    def test_run(self, mock_polling):
        self.bot.run()
        mock_polling.assert_called_once_with(
            self.bot.dp, 
            skip_updates=True,
            on_startup=unittest.mock.ANY,
            on_shutdown=unittest.mock.ANY
        )

if __name__ == '__main__':
    unittest.main()